#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Union, Dict, Any
from quark.torch.quantization.utils import calculate_qmin_qmax
from quark.torch.quantization.config.type import Dtype, RoundType


@dataclass(eq=True)
class QuantConfig:
    dtype: str
    qscheme: Optional[str] = None
    ch_axis: Optional[int] = None
    group_size: Optional[int] = None
    quant_min: Union[int, float, None] = None
    quant_max: Union[int, float, None] = None
    round_method: Optional[int] = None

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> QuantConfig:
        dtype = config_dict["dtype"]
        quant_min, quant_max = calculate_qmin_qmax(Dtype(dtype))

        qscheme = config_dict["qscheme"] if config_dict.get("qscheme", None) is not None else None
        round_method = int(RoundType[config_dict["round_method"]].value) if config_dict.get("round_method",
                                                                                            None) is not None else None
        ch_axis = config_dict["axis"] if config_dict.get("axis", None) is not None else None
        group_size = config_dict["group_size"] if config_dict.get("group_size", None) is not None else None
        return cls(dtype=dtype,
                   qscheme=qscheme,
                   ch_axis=ch_axis,
                   group_size=group_size,
                   quant_min=quant_min,
                   quant_max=quant_max,
                   round_method=round_method)
