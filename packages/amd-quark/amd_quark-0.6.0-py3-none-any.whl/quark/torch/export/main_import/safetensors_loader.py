#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

from typing import Union, Optional, Dict, List, Any
import json
from pathlib import Path
import torch
from quark.shares.utils.log import ScreenLogger, log_errors
from quark.torch.export.utils import find_patterns_groups

logger = ScreenLogger(__name__)

SAFE_WEIGHTS_NAME = "model.safetensors"
SAFE_WEIGHTS_INDEX_NAME = "model.safetensors.index.json"

AWQ_TENSORS_MAP = {
    "weight": "weight",
    "qweight": "qweight",
    "weight_scale": "scales",
    "weight_zero_point": "qzeros",
    "bias": "bias"
}

QUARK_TENSORS_MAP = {
    "weight": "weight",
    "qweight": "weight",
    "weight_scale": "weight_scale",
    "weight_zero_point": "weight_zero_point",
    "bias": "bias",
    "bias_scale": "bias_scale",
    "bias_zero_point": "bias_zero_point",
    "input_scale": "input_scale",
    "input_zero_point": "input_zero_point",
    "output_scale": "output_scale",
    "output_zero_point": "output_zero_point",
}


class SafetensorsLoader:

    @log_errors
    def __init__(self, pretrained_dir: Union[str, Path], custom_mode: str) -> None:
        safetensors_dir = Path(pretrained_dir)
        safetensors_path = safetensors_dir / SAFE_WEIGHTS_NAME
        safetensors_index_path = safetensors_dir / SAFE_WEIGHTS_INDEX_NAME
        self.custom_mode = custom_mode
        self._is_shared = None
        self._state_dict: Dict[str, torch.Tensor] = {}
        self._ops_names: List[str] = []
        if safetensors_path.exists():
            self._is_shared = False
            self._state_dict = self.load_state_dict(str(safetensors_path))
        elif safetensors_index_path.exists():
            self._is_shared = True
            with open(str(safetensors_index_path), "r") as file:
                safetensors_indices = json.load(file)
            safetensors_files = [value for key, value in safetensors_indices["weight_map"].items()]
            safetensors_files = list(set(safetensors_files))
            for filename in safetensors_files:
                filepath = safetensors_dir / filename
                self._state_dict.update(self.load_state_dict(str(filepath)))
        else:
            raise FileNotFoundError("Safetensors file does not exist")

        if self._has_dbrx_experts():
            self._split_params_for_DbrxExperts()

        tensor_names = list(self._state_dict.keys())
        ops_names = ['.'.join(name.split('.')[:-1]) for name in tensor_names]
        self._ops_names = list(set(ops_names))

    def _has_dbrx_experts(self) -> bool:
        self.dbrx_experts_groups: List[List[str]] = []
        dbrx_params_name = [["*ffn.experts.mlp.v1_weight", "*ffn.experts.mlp.v1_weight_scale"],
                            ["*ffn.experts.mlp.w1_weight", "*ffn.experts.mlp.w1_weight_scale"],
                            ["*ffn.experts.mlp.w2_weight", "*ffn.experts.mlp.w2_weight_scale"]]

        params_name = list(self._state_dict.keys())
        self.dbrx_experts_groups = find_patterns_groups(dbrx_params_name, params_name)
        return True if len(self.dbrx_experts_groups) > 0 else False

    def _split_params_for_DbrxExperts(self) -> None:
        params_name = list(self._state_dict.keys())
        for group in self.dbrx_experts_groups:
            for name in group:
                if "weight_scale" in name.split(".")[-1]:
                    weight_scale_name = name
                else:
                    weight_name = name
            mlp_suffix = weight_name.rsplit("_", 1)
            mlp_suffix[-1] = mlp_suffix[-1].replace("weight", "input_scale")
            input_scale_name = "_".join(mlp_suffix)
            input_scale_exist = True if input_scale_name in params_name else False

            mlp_suffix[-1] = mlp_suffix[-1].replace("input_scale", "output_scale")
            output_scale_name = "_".join(mlp_suffix)
            output_scale_exist = True if output_scale_name in params_name else False

            weight_tensor = self._state_dict[weight_name]
            weight_scale_tensor = self._state_dict[weight_scale_name]
            experts_num = weight_scale_tensor.shape[0]
            weight_chunk = torch.chunk(weight_tensor, experts_num)

            mlp_name = weight_name.split(".")[:-1]
            suffix_name = weight_name.split(".")[-1]
            param_name = suffix_name.split("_")[0]

            for i, item in enumerate(weight_chunk):
                weight_name_list = mlp_name + [str(i), param_name, "weight"]
                weight_scale_name_list = mlp_name + [str(i), param_name, "weight_scale"]

                weight_i_name = ".".join(weight_name_list)
                weight_scale_i_name = ".".join(weight_scale_name_list)

                self._state_dict[weight_scale_i_name] = weight_scale_tensor[i]
                if "w2" in suffix_name:
                    self._state_dict[weight_i_name] = item.t().contiguous()
                else:
                    self._state_dict[weight_i_name] = item

                if input_scale_exist:
                    input_scale_name_list = mlp_name + [str(i), param_name, "input_scale"]
                    input_scale_i_name = ".".join(input_scale_name_list)
                    self._state_dict[input_scale_i_name] = self._state_dict[input_scale_name][i]

                if output_scale_exist:
                    output_scale_name_list = mlp_name + [str(i), param_name, "output_scale"]
                    output_scale_i_name = ".".join(output_scale_name_list)
                    self._state_dict[output_scale_i_name] = self._state_dict[output_scale_name][i]

            self._state_dict.pop(weight_name)
            self._state_dict.pop(weight_scale_name)
            self._state_dict.pop(input_scale_name, None)
            self._state_dict.pop(output_scale_name, None)

    @staticmethod
    def load_state_dict(checkpoint_file: str) -> Dict[str, Any]:
        from safetensors.torch import load_file as safe_load_file
        return safe_load_file(checkpoint_file)  # type: ignore

    def get_tensor(self, op_name: str, tensor_type: str = "qweight") -> Optional[torch.Tensor]:
        tensors_suffix_map = QUARK_TENSORS_MAP
        if self.custom_mode == "awq":
            tensors_suffix_map = AWQ_TENSORS_MAP
        if tensor_type not in tensors_suffix_map.keys():
            return None
        tensor_suffix = tensors_suffix_map[tensor_type]
        tensor_name = op_name + '.' + tensor_suffix
        if tensor_name not in self.state_dict.keys():
            return None
        return self.state_dict[tensor_name]

    @property
    def state_dict(self) -> Dict[str, torch.Tensor]:
        return self._state_dict

    @property
    def ops_name(self) -> List[str]:
        return self._ops_names
