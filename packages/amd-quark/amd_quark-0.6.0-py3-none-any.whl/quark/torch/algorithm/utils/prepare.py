#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

from __future__ import annotations
import torch
from typing import List, Tuple, Any, Dict, cast, Union, Iterator, Optional
import torch.nn as nn
from quark.torch.algorithm.utils.module import get_device, move_to_device
from quark.torch.algorithm.utils.utils import clear_memory
from quark.torch.algorithm.utils.module import get_nested_attr_from_module
import inspect


def cache_model_inps(model: nn.Module, modules: nn.ModuleList,
                     samples: List[Dict[str, Any]]) -> Tuple[nn.ModuleList, Dict[str, Any], List[torch.Tensor]]:

    inps: List[torch.Tensor] = []
    layer_args: List[Union[torch.Tensor, None]] = []
    layer_kwargs: Dict[str, Any] = {}

    # get input and kwargs to layer 0
    # with_kwargs is only supported in PyTorch 2.0
    # use this Catcher hack for now
    class Catcher(nn.Module):

        def __init__(self, module: nn.Module, inps: List[torch.Tensor], layer_args: List[Union[torch.Tensor, None]],
                     layer_kwargs: Dict[str, Any]) -> None:
            super().__init__()
            self.module = module
            self.inps = inps
            self.layer_args = layer_args
            self.layer_kwargs = layer_kwargs

        def forward(self, *args: torch.Tensor, **kwargs: Any) -> None:
            # assume first input to forward is hidden states
            if len(args) > 0:
                hidden_states = args[0]
                if len(self.layer_args) == 0:
                    self.layer_args.extend(
                        args[1:]
                    )  # For attention_mask and rotary_pos_emb, the value of the new input is always same, so it is kept once
            else:
                first_key = list(kwargs.keys())[0]
                hidden_states = kwargs.pop(first_key)

            self.inps.append(hidden_states)
            self.layer_kwargs.update(kwargs)
            raise ValueError  # early exit to break later inference

        # patch layer 0 to catch input and kwargs

    cur_layer_device = get_device(modules[0])
    required_kwargs = inspect.signature(modules[0].forward).parameters
    modules[0] = Catcher(modules[0], inps, layer_args, layer_kwargs)
    for sample in samples:
        if isinstance(sample, torch.Tensor):
            try:
                model(sample)
            except ValueError:  # work with early exit
                pass
        else:
            for k, v in sample.items():
                if len(v.shape) == 1:
                    v = v.unsqueeze(0)
                sample[k] = move_to_device(v, cur_layer_device)
            try:
                model(**sample)
            except ValueError:  # work with early exit
                pass
    del samples
    modules[0] = modules[0].module  # restore

    clear_memory()
    layer_args_iter: Iterator[Optional[torch.Tensor]] = iter(layer_args)
    for k, v in required_kwargs.items():
        if k == "hidden_states" or k in layer_kwargs or v.kind == v.VAR_KEYWORD:
            continue
        else:
            layer_kwargs[k] = next(layer_args_iter, None)
    return modules, layer_kwargs, inps


def move_embed(model: nn.Module, embedding_layer_name_list: List[str], device: Union[Dict[str, torch.device],
                                                                                     torch.device]) -> None:
    for embedding_layer_name in embedding_layer_name_list:
        embedding_layer = get_nested_attr_from_module(model, embedding_layer_name)
        if isinstance(device, dict):
            embedding_layer = embedding_layer.to(device[embedding_layer_name])
        else:
            embedding_layer = embedding_layer.to(device)


def get_layers_for_scaling(module: nn.Module, input_feat: Dict[str, Any], module_kwargs: Dict[str, Any],
                           scaling_layers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    layers: List[Dict[str, Any]] = []
    has_kwargs = True  # For first layer from module, input kwargs.

    for layer in scaling_layers:
        if layer[
                'inp'] in input_feat:  # for moe models that skip unselected moe layers, unselected moe layers have not "inp"
            if "condition" in layer:
                condition_result = eval(layer["condition"])
                if not condition_result:
                    continue

            linear_layers = []
            for i in range(len(layer['layers'])):
                linear_layers.append(get_nested_attr_from_module(module, layer['layers'][i]))

            layer_dict = dict(
                prev_op=get_nested_attr_from_module(module, layer['prev_op']),
                layers=linear_layers,
                inp=input_feat[layer['inp']],
            )

            if 'module2inspect' in layer and layer['module2inspect'] is not None:
                if layer['module2inspect'] == '':
                    layer_dict['module2inspect'] = module
                else:
                    layer_dict['module2inspect'] = get_nested_attr_from_module(module, layer['module2inspect'])
            if has_kwargs:
                layer_dict['kwargs'] = module_kwargs
                has_kwargs = False

            layers.append(layer_dict)

    return layers


def get_model_layers(model: nn.Module, layers_name: str) -> nn.ModuleList:
    model_layer = get_nested_attr_from_module(model, layers_name)
    return cast(nn.ModuleList, model_layer)


def init_device_map(model: nn.Module) -> dict[str, torch.device]:
    from collections import defaultdict
    k_name_v_device: dict[Any, torch.device] = {}
    if hasattr(model, 'hf_device_map'):
        if len(model.hf_device_map) == 1:
            device = [v for _, v in model.hf_device_map.items()][0]
            k_name_v_device = defaultdict(lambda: device)
        else:
            k_name_v_device = {
                layer_name:
                (torch.device(layer_device) if isinstance(layer_device, str) else torch.device(f'cuda:{layer_device}'))
                for layer_name, layer_device in model.hf_device_map.items()
            }
    else:
        # it is needed
        device = model.device
        k_name_v_device = defaultdict(lambda: device)
    return k_name_v_device
