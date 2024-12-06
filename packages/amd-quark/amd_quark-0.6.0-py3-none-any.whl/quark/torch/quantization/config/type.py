#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

from enum import Enum, auto


class QSchemeType(Enum):
    """
    The quantization schemes applicable to tensors within a model.

    - `per_tensor`: Quantization is applied uniformly across the entire tensor.
    - `per_channel`: Quantization parameters differ across channels of the tensor.
    - `per_group`: Quantization parameters differ across defined groups of weight tensor elements.

    """

    per_tensor = "per_tensor"
    per_channel = "per_channel"
    per_group = "per_group"


class ZeroPointType(Enum):
    """
    The zero point Dtype used for zero point.

    - 'int32': int zero point
    - 'float32': float zero point
    """
    int32 = "int32"
    float32 = "float32"


class Dtype(Enum):
    """
    The data types used for quantization of tensors.

    - `int8`: Signed 8-bit integer, range from -128 to 127.
    - `uint8`: Unsigned 8-bit integer, range from 0 to 255.
    - `int4`: Signed 4-bit integer, range from -8 to 7.
    - `uint4`: Unsigned 4-bit integer, range from 0 to 15.
    - `bfloat16`: Bfloat16 format.
    - `float16`: Standard 16-bit floating point format.
    - `fp8_e4m3`: FP8 format with 4 exponent bits and 3 bits of mantissa.
    - `fp8_e5m2`: FP8 format with 5 exponent bits and 2 bits of mantissa.
    - `fp6_e3m2`: FP6 format with 3 exponent bits and 2 bits of mantissa.
    - `fp6_e2m3`: FP6 format with 2 exponent bits and 3 bits of mantissa.
    - `fp4`: FP4 format.
    - `mx`: MX format 8 bit shared exponent with specific element data types.
    - `mx6`, `mx9`: Block data representation with multi-level ultra-fine scaling factors.

    """
    int8 = "int8"
    uint8 = "uint8"
    int4 = "int4"
    uint4 = "uint4"
    int2 = "int2"
    bfloat16 = "bfloat16"
    float16 = "float16"
    fp8_e5m2 = "fp8_e5m2"
    fp8_e4m3 = "fp8_e4m3"
    fp6_e3m2 = "fp6_e3m2"
    fp6_e2m3 = "fp6_e2m3"
    fp4 = "fp4"
    mx = "mx"
    mx6 = "mx6"
    mx9 = "mx9"
    bfp16 = "bfp16"

    @staticmethod
    def from_str(s: str) -> "Dtype":
        assert (s is not None), "String dtype is None"
        s = s.lower()
        if hasattr(Dtype, s):
            return getattr(Dtype, s)  # type: ignore
        else:
            raise Exception("Undefined dtype", s)

    def to_bitwidth(self) -> int:  # pragma: no cover
        if self.value in ["int8", "uint8", "fp8_e5m2", "fp8_e4m3", "mx"]:
            return 8
        elif self.value in ["int4", "uint4", "fp4"]:
            return 4
        elif self.value in ["bfloat16", "float16"]:
            return 16
        elif self.value in ["int2"]:
            return 2
        elif self.value in ["fp6_e3m2", "fp6_e2m3", "mx6"]:
            return 6
        elif self.value in ["mx9"]:
            return 9
        else:
            raise ValueError("Unknown Dtype")


class ScaleType(Enum):
    """
    The types of scales used in quantization.

    - `float`: Scale values are floating-point numbers.
    - `pof2`: Scale values are powers of two.

    """
    float = auto()
    pof2 = auto()


class RoundType(Enum):
    """
    The rounding methods used during quantization.

    - `round`: Rounds.
    - `floor`: Floors towards the nearest even number.
    - `half_even`: Rounds towards the nearest even number.

    """
    round = 2
    floor = 3
    half_even = 8


class DeviceType(Enum):
    """
    The target devices for model deployment and optimization.

    - `CPU`: CPU.
    - `IPU`: IPU.
    """
    CPU = "cpu"
    IPU = "ipu"


class QuantizationMode(Enum):
    """
    Different quantization modes.

    - `eager_mode`: The eager mode based on PyTorch in-place operator replacement.
    - `fx_graph_mode`: The graph mode based on torch.fx.
    """
    eager_mode = auto()
    fx_graph_mode = auto()


class TQTThresholdInitMeth(Enum):
    """
    The method of threshold initialization of TQT algorithm in QAT. See Table 2 in https://arxiv.org/pdf/1903.08066.pdf

    - `_3SD`: The method of threshold initialization with std and 3 as hyperparameters.
    - `_LL_J`: The method of threshold initialization in the Algorithm 1 of paper "Quantizing Convolutional Neural Networks for Low-Power High-Throughput Inference Engines" - Sean Settle et al. https://arxiv.org/pdf/1805.07941.pdf
    """
    _3SD = '_3sd'
    _KL_J = '_kl_j'
