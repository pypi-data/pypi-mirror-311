#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
"""Quark Algorithm/Pre-Quant Optimization API for PyTorch."""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, List, Optional, Union
from quark.shares.utils.log import ScreenLogger
from quark.torch.quantization.config.config import Config
from quark.torch.pruning.config import Config as Pruning_Config
from quark.torch.quantization.tensor_quantize import ScaledFakeQuantize
from quark.torch.algorithm.utils.auto_config import is_auto_config_needed, add_auto_config
from quark.torch.algorithm.awq.awq import AwqProcessor
from quark.torch.algorithm.awq.smooth import SmoothQuantProcessor
from quark.torch.algorithm.rotation.rotation import RotationProcessor
from quark.torch.algorithm.gptq.gptq import GptqProcessor
from quark.torch.algorithm.osscar.osscar import OsscarProcessor
from quark.torch.algorithm.awq.auto_smooth import AutoSmoothQuantProcessor

logger = ScreenLogger(__name__)

__all__ = ["apply_pre_quantization_optimization", "apply_advanced_quant_algo", "apply_advanced_pruning_algo"]

PROCESSOR_MAP = {
    'rotation': RotationProcessor,
    'smooth': SmoothQuantProcessor,
    'autosmoothquant': AutoSmoothQuantProcessor,
    'awq': AwqProcessor,
    'gptq': GptqProcessor,
    'osscar': OsscarProcessor
}


@torch.no_grad()
def apply_pre_quantization_optimization(
    model: nn.Module,
    config: Config,
    dataloader: Optional[Union[DataLoader[torch.Tensor], DataLoader[List[Dict[str, torch.Tensor]]],
                               DataLoader[Dict[str, torch.Tensor]]]] = None
) -> nn.Module:
    if config.pre_quant_opt_config is not None:
        logger.info("Pre-quantization optimization start.")

        if not isinstance(config.pre_quant_opt_config, List):
            pre_quant_opts = [config.pre_quant_opt_config]
        else:
            pre_quant_opts = config.pre_quant_opt_config

        for pre_quant_opt_config in pre_quant_opts:
            pre_quant_optimizer = PROCESSOR_MAP[pre_quant_opt_config.name](model, pre_quant_opt_config, dataloader)
            pre_quant_optimizer.apply()

        logger.info("Pre-quantization optimization end.")
    return model


@torch.no_grad()
def apply_advanced_quant_algo(
    model: nn.Module,
    config: Config,
    is_accelerate: Optional[bool],
    dataloader: Optional[Union[DataLoader[torch.Tensor], DataLoader[List[Dict[str, torch.Tensor]]],
                               DataLoader[Dict[str, torch.Tensor]]]] = None
) -> nn.Module:
    if config.algo_config is not None:
        logger.info("Advanced algorithm start.")
        device_map = {"": model.device}
        if is_accelerate:
            device_map = model.hf_device_map

        for module in model.modules():
            if isinstance(module, ScaledFakeQuantize):
                module.disable_fake_quant()
                module.disable_observer()

        quantizer = PROCESSOR_MAP[config.algo_config.name](model, config.algo_config, dataloader)
        quantizer.apply()

        if len(device_map) == 1 and "" in device_map.keys():
            model = model.to(device_map[""])
        else:
            for name, module in model.named_modules(remove_duplicate=False):
                if name in device_map:
                    module.to(torch.device(device_map[name])) if isinstance(device_map[name], int) else model.to(
                        device_map[name])
        logger.info("Advanced algorithm end.")
    return model


def add_algorithm_config_by_model(model: nn.Module,
                                  dataloader: Union[DataLoader[torch.Tensor], DataLoader[List[Dict[str, torch.Tensor]]],
                                                    DataLoader[Dict[str,
                                                                    torch.Tensor]], None], config: Config) -> Config:
    # Determine the positions and need for auto configuration
    smooth_position, rotation_position, is_awq_needed = is_auto_config_needed(config)

    # If any configuration is needed, proceed with auto configuration
    if smooth_position >= 0 or rotation_position >= 0 or is_awq_needed:
        assert dataloader is not None, "Dataloader must be provided when auto-configuration is needed."
        # Get a sample input from the dataloader
        dummy_input = next(iter(dataloader))
        # Add auto-generated configurations to the existing config
        config = add_auto_config(model, dummy_input, config, smooth_position, rotation_position, is_awq_needed)

    return config


@torch.no_grad()
def apply_advanced_pruning_algo(
    model: nn.Module,
    config: Pruning_Config,
    is_accelerate: Optional[bool],
    dataloader: Optional[Union[DataLoader[torch.Tensor], DataLoader[List[Dict[str, torch.Tensor]]],
                               DataLoader[Dict[str, torch.Tensor]]]] = None
) -> nn.Module:
    if config.algo_config is not None:
        logger.info("Advanced pruning algorithm start.")
        device_map = {"": model.device}
        if is_accelerate:
            device_map = model.hf_device_map

        pruner = PROCESSOR_MAP[config.algo_config.name](model, config.algo_config, dataloader)
        pruner.apply()

        if len(device_map) == 1 and "" in device_map.keys():
            model = model.to(device_map[""])
        else:
            for name, module in model.named_modules(remove_duplicate=False):
                if name in device_map:
                    module.to(torch.device(device_map[name])) if isinstance(device_map[name], int) else model.to(
                        device_map[name])
        logger.info("Advanced pruning algorithm end.")
    return model
