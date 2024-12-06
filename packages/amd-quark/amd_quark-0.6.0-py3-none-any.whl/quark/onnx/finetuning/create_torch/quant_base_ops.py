#
# Copyright (C) 2023, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#

import torch
import numpy
from abc import ABC, abstractmethod
from typing import Optional, Union, Tuple, Dict, Any, List

from .quant_base_fns import BFPQuantizer as FNQuantizer


class RoundHalfToEven(torch.autograd.Function):

    @staticmethod
    def forward(ctx: torch.autograd.Function, t: torch.Tensor) -> torch.Tensor:
        return torch.round(t)

    @staticmethod  # type: ignore
    def backward(ctx: torch.autograd.Function, grad_output: torch.Tensor) -> torch.Tensor:
        grad_input = grad_output.clone()
        return grad_input


class BaseQuantFunction(torch.autograd.Function):

    @staticmethod
    def forward(ctx: Any, tensor: torch.Tensor, scale: torch.Tensor, zero_point: torch.Tensor, min_q: torch.Tensor,
                max_q: torch.Tensor, round_func: Any) -> torch.Tensor:
        quant_t = round_func(tensor / scale) + zero_point

        # Save context for backward
        # gradient == 1
        grad_mask = torch.le(quant_t, max_q) & torch.ge(quant_t, min_q)
        # gardient == 0.5 at clip boundary, for maximum and minmum
        grad_mask_clip_boundary = (quant_t == max_q) | (quant_t == min_q)
        ctx.save_for_backward(grad_mask, grad_mask_clip_boundary, scale)

        quant_t = torch.minimum(torch.maximum(quant_t, min_q), max_q)
        # quant_t = torch.clamp(quant_t, min_q, max_q)

        return quant_t

    @staticmethod  # type: ignore
    def backward(ctx: Any, grad_output: torch.Tensor) -> Tuple[Optional[torch.Tensor], None, None, None, None, None]:
        grad_mask, grad_mask_clip_boundary, scale = ctx.saved_tensors

        grad_input = grad_output * grad_mask
        grad_input = grad_input * (1.0 - grad_mask_clip_boundary.to(torch.float32) + grad_mask_clip_boundary * 0.5)
        grad_input = grad_input / scale

        return grad_input, None, None, None, None, None


class BaseDeQuantFunction(torch.autograd.Function):

    @staticmethod
    def forward(ctx: torch.autograd.Function, tensor: torch.Tensor, scale: torch.Tensor,
                zero_point: torch.Tensor) -> torch.Tensor:
        ctx.save_for_backward(scale)
        ctx.save_for_backward(zero_point)
        return (tensor - zero_point) * scale

    @staticmethod  # type: ignore
    def backward(ctx: torch.autograd.Function, grad_output: torch.Tensor) -> Tuple[torch.Tensor, None, None]:
        scale = ctx.saved_tensors
        zero_point = ctx.saved_tensors
        return (grad_output - zero_point) * scale, None, None


class BaseQuantDequantFunction(torch.autograd.Function):

    @staticmethod
    def forward(ctx: Any, tensor: torch.Tensor, scale: torch.Tensor, zero_point: torch.Tensor, min_q: torch.Tensor,
                max_q: torch.Tensor, round_func: Any) -> torch.Tensor:
        quant_t = round_func(tensor / scale) + zero_point
        # quant_t = torch.minimum(torch.maximum(quant_t, min_q), max_q)

        # Save context for backward
        grad_mask = torch.le(quant_t, max_q) & torch.ge(quant_t, min_q)
        # gardient == 0.5 at clip boundary, for maximum and minmum
        grad_mask_clip_boundary = (quant_t == max_q) | (quant_t == min_q)
        ctx.save_for_backward(grad_mask, grad_mask_clip_boundary)

        quant_t = (torch.clamp(quant_t, min_q, max_q) - zero_point) * scale
        quant_t = quant_t.to(tensor.dtype)

        return quant_t

    @staticmethod  # type: ignore
    def backward(ctx: Any, grad_output: torch.Tensor) -> Tuple[torch.Tensor, None, None, None, None, None]:
        grad_mask, grad_mask_clip_boundary = ctx.saved_tensors
        grad_input = grad_output * grad_mask
        grad_input = grad_input * (1.0 - grad_mask_clip_boundary.to(torch.float32) + grad_mask_clip_boundary * 0.5)
        return grad_output, None, None, None, None, None


class INTQuantFunction(torch.autograd.Function):

    @staticmethod
    def forward(ctx: torch.autograd.Function, tensor: torch.Tensor, scale: torch.Tensor, zero_point: torch.Tensor,
                min_q: torch.Tensor, max_q: torch.Tensor, round_func: torch.autograd.Function) -> torch.Tensor:
        quant_t = round_func(tensor / scale) + zero_point

        # quant_t = torch.minimum(torch.maximum(quant_t, min_q), max_q)
        quant_t = torch.clamp(quant_t, min_q, max_q)

        return quant_t

    @staticmethod  # type: ignore
    def backward(ctx: torch.autograd.Function,
                 grad_output: torch.Tensor) -> Tuple[torch.Tensor, None, None, None, None, None]:
        return grad_output, None, None, None, None, None


class INTDeQuantFunction(torch.autograd.Function):

    @staticmethod
    def forward(ctx: Any, tensor: torch.Tensor, scale: torch.Tensor, zero_point: torch.Tensor) -> torch.Tensor:
        ctx.save_for_backward(scale, zero_point)
        return (tensor - zero_point) * scale

    @staticmethod  # type: ignore
    def backward(ctx: Any, grad_output: torch.Tensor) -> Tuple[torch.Tensor, None, None]:
        scale, zero_point = ctx.saved_tensors
        return (grad_output - zero_point) * scale, None, None


class INTQuantDequantFunction(torch.autograd.Function):

    @staticmethod
    def forward(ctx: torch.autograd.Function, tensor: torch.Tensor, scale: torch.Tensor, zero_point: torch.Tensor,
                min_q: torch.Tensor, max_q: torch.Tensor, round_func: torch.autograd.Function) -> torch.Tensor:
        quant_t = round_func(tensor / scale) + zero_point
        quant_t = (torch.clamp(quant_t, min_q, max_q) - zero_point) * scale
        return quant_t

    @staticmethod  # type: ignore
    def backward(ctx: torch.autograd.Function,
                 grad_output: torch.Tensor) -> Tuple[torch.Tensor, None, None, None, None, None]:
        grad_input = grad_output.clone()
        return grad_input, None, None, None, None, None


# Note that these functions are not traceable
default_round_func = RoundHalfToEven.apply
int_quant_func = INTQuantFunction.apply
int_dequant_func = INTDeQuantFunction.apply


# Followed pylight, we use a common function to implement quantize-dequantize
def int_quant_dequant_func(tensor: torch.Tensor, scale: torch.Tensor, zero_point: torch.Tensor, min_q: torch.Tensor,
                           max_q: torch.Tensor, round_func: Any) -> torch.Tensor:
    quant_t = round_func(tensor / scale) + zero_point
    quant_t = (torch.clamp(quant_t, min_q, max_q) - zero_point) * scale
    return quant_t


class Quantizer(torch.nn.Module):
    """ Standard Quantizer has three functions including quantize,
    dequantize and quantize_dequantize, which is corresponding to ONNX
    QuantizeLinear, DequantizeLinear and Q/DQ pair separately.
    By default in forward, it works in quantize_dequantize mode.
    """

    def __init__(self,
                 scale: torch.Tensor,
                 zero_point: torch.Tensor,
                 min_q: torch.Tensor,
                 max_q: torch.Tensor,
                 ch_axis: int = 0,
                 q_folded: bool = False) -> None:
        super().__init__()

        self.scale = scale
        self.zero_point = zero_point
        self.min_q = min_q
        self.max_q = max_q

        # This is for per-channel quantization to specify the axis of the channel.
        # per-channel is usually used for weight, so the default value of axis is 0.
        self.ch_axis = ch_axis

        # This is a flag to indicate QuantizeLinear in QDQ pair was foled or not.
        # If true, you may need dequantize the tensor to 'restore' its original values,
        # for example, to restore original bias (but actually there is a loss)
        self.q_folded = q_folded

    def round_impl(self, tensor: torch.Tensor) -> None:
        """ Implement the round function, designed for adaround quantizer """
        self.round_func = default_round_func

    def _to_device(self, tensor: torch.Tensor) -> None:
        """ Set the device of quantization parameters as the tensor """
        self.scale = self.scale.to(device=tensor.device)
        self.zero_point = self.zero_point.to(device=tensor.device)
        self.min_q = self.min_q.to(device=tensor.device)
        self.max_q = self.max_q.to(device=tensor.device)

    def _broad_cast(self, param: torch.Tensor, tensor: torch.Tensor) -> torch.Tensor:
        """ This method takes a 1-dimension parameter and n-dimension tensor.
        The parameter is broad-casted to match the n-dimensional tensor """
        assert len(param.shape) <= 1  # Should be 1-dimensional tensor (scalar or vector)

        # No need broad cast for per_tensor
        if param.numel() == 1:
            return param

        # Original ch_axis could be a negative value
        ch_axis = self.ch_axis + len(tensor.shape) if self.ch_axis < 0 else self.ch_axis

        # Shape of parameter should match the channel dimension of the input tensor
        assert param.numel() == tensor.shape[ch_axis]

        # Have same dimensions with the tensor, each axis will be 1 except ch_axis
        shape = tuple(dim if axis == ch_axis else 1 for axis, dim in enumerate(tensor.shape))

        return param.view(shape)

    def tensor_sync(self, tensor: torch.Tensor) -> None:
        """ The Pre-processing of the parameter according to the input tensor """
        self._to_device(tensor)

        if len(self.scale.shape) <= 1:
            self.scale = self._broad_cast(self.scale, tensor)
        if len(self.zero_point.shape) <= 1:
            self.zero_point = self._broad_cast(self.zero_point, tensor)

    def quantize(self, tensor: torch.Tensor) -> Any:
        self.tensor_sync(tensor)
        self.round_impl(tensor)
        return int_quant_func(tensor, self.scale, self.zero_point, self.min_q, self.max_q, self.round_func)

    def dequantize(self, tensor: torch.Tensor) -> Any:
        self.tensor_sync(tensor)
        return int_dequant_func(tensor, self.scale, self.zero_point)

    def quantize_dequantize(self, tensor: torch.Tensor) -> torch.Tensor:
        self.tensor_sync(tensor)
        self.round_impl(tensor)
        return int_quant_dequant_func(tensor, self.scale, self.zero_point, self.min_q, self.max_q, self.round_func)

    def forward(self, tensor: torch.Tensor) -> torch.Tensor:
        return self.quantize_dequantize(tensor)


class AdaroundConstants:
    """ Constants used for Adarounding """
    GAMMA = -0.1
    ZETA = 1.1


class AdaroundQuantizer(Quantizer):
    """ AdaRound Quantizer has a alpha paramter for optimizing weight rounding """

    def __init__(self,
                 scale: torch.Tensor,
                 zero_point: torch.Tensor,
                 min_q: torch.Tensor,
                 max_q: torch.Tensor,
                 ch_axis: int = 0,
                 q_folded: bool = False) -> None:
        super().__init__(scale, zero_point, min_q, max_q, ch_axis=ch_axis, q_folded=q_folded)

        self.alpha: Optional[torch.nn.Parameter] = None
        self.use_soft_rounding = True

    def round_impl(self, tensor: torch.Tensor) -> None:
        """
        Implement the rounding function for adaround
        :param weight: The tensor to be ada-rounded
        """
        if self.alpha is None:
            self.initialize_alpha(tensor)

        assert self.alpha is not None, "self.alpha is None"
        alpha = self.alpha.to(device=tensor.device, dtype=tensor.dtype)
        h_alpha = self._get_h_alpha(alpha).to(tensor.dtype)
        self.round_func = lambda input: torch.floor(input) + h_alpha  # type: ignore

    def initialize_alpha(self, tensor: torch.Tensor) -> None:
        """
        Initializes alpha parameter, same shape as the tensor
        :param tensor: The tensor to be ada-rounded
        """
        if self.alpha is not None:
            return

        tensor_floor = torch.floor(tensor / self.scale)

        tensor_diff = (tensor / self.scale) - tensor_floor
        alpha = -torch.log((AdaroundConstants.ZETA - AdaroundConstants.GAMMA) /
                           (tensor_diff - AdaroundConstants.GAMMA) - 1)

        # Even if the input is integer type, alpha has to be kept in float32
        # in order to be updated by the optimizer
        self.alpha = torch.nn.Parameter(alpha.float(), requires_grad=True)

    def _get_h_alpha(self, alpha: torch.Tensor) -> torch.Tensor:
        """
        Calculate h_alpha tensor
        :return: the h_alpha tensor
        """
        # Soft rounding maps alpha parameter between zero and one using
        # rectified sigmoid function and hard rounding maps it to exactly zero or one
        if self.use_soft_rounding:
            h_alpha = torch.clamp(
                torch.sigmoid(alpha) * (AdaroundConstants.ZETA - AdaroundConstants.GAMMA) + AdaroundConstants.GAMMA, 0,
                1)
        else:
            h_alpha = (alpha >= 0)
        return h_alpha


class QuantizationModule(torch.nn.Module):
    """ A pytorch module that behaves as ONNX quantization nodes """

    def __init__(
        self, quant_info: Union[Tuple[numpy.typing.NDArray[numpy.float32], numpy.typing.NDArray[Any],
                                      numpy.typing.NDArray[Any], numpy.typing.NDArray[Any], int, bool], Dict[str, Any],
                                None]
    ) -> None:
        super().__init__()

        self.quantizer: Optional[Union[Quantizer, FNQuantizer]] = None

        if isinstance(quant_info, dict):
            self.quantizer = FNQuantizer(quant_info)
        elif isinstance(quant_info, tuple):
            self.quantizer = Quantizer(torch.from_numpy(quant_info[0]), torch.from_numpy(quant_info[1]),
                                       torch.from_numpy(quant_info[2]), torch.from_numpy(quant_info[3]), quant_info[4],
                                       quant_info[5])
        else:
            raise ValueError("Invalid quantization info: {}".format(quant_info))

    def forward(self, tensor: torch.Tensor) -> Any:
        if self.quantizer is None:
            return tensor
        else:
            return self.quantizer(tensor)


class QuantizeWrapper(torch.nn.Module, ABC):
    """ A wrapper for torch layer's input/weight/bias quantization """

    def __init__(self, w_alpha: float = 1.0, b_beta: float = 1.0, **kwargs: Dict[str, Any]) -> None:
        super().__init__(**kwargs)

        # These parameters are used to implement ONNX Gemm op's formula,
        # and compatiable with other ops since their default values are 1
        self.w_alpha: float = w_alpha
        self.b_beta: float = b_beta

        self.input_quantizer: Optional[Union[Quantizer, FNQuantizer]] = None
        self.weight_quantizer: Optional[Union[Quantizer, FNQuantizer]] = None
        self.bias_quantizer: Optional[Union[Quantizer, FNQuantizer]] = None

        # This quantize wrapper is for the modules that should have weight
        assert hasattr(self, 'weight') and f'{type(self)} does not contain weight'

        # This is a flag to indicate if we have a accuracy improvement after optimization.
        # If false, do not to get the optimized weight or bias from the wrapperred module.
        self.opt_gained: Optional[bool] = None

    def create_input_qdq_quantizer(self,
                                   scale: torch.Tensor,
                                   zero_point: torch.Tensor,
                                   min_q: torch.Tensor,
                                   max_q: torch.Tensor,
                                   ch_axis: int = 0,
                                   q_folded: bool = False) -> None:
        # Activation should have QuantizeLinear and DequantizeLinear pair
        self.input_quantizer = Quantizer(scale, zero_point, min_q, max_q, ch_axis, q_folded)

    def create_weight_qdq_quantizer(self,
                                    scale: torch.Tensor,
                                    zero_point: torch.Tensor,
                                    min_q: torch.Tensor,
                                    max_q: torch.Tensor,
                                    ch_axis: int = 0,
                                    q_folded: bool = False) -> None:
        # QuantizeLinear may be folded for weight
        self.weight_quantizer = Quantizer(scale, zero_point, min_q, max_q, ch_axis, q_folded)

    def create_bias_qdq_quantizer(self,
                                  scale: torch.Tensor,
                                  zero_point: torch.Tensor,
                                  min_q: torch.Tensor,
                                  max_q: torch.Tensor,
                                  ch_axis: int = 0,
                                  q_folded: bool = False) -> None:
        # QuantizeLinear always be folded for bias
        self.bias_quantizer = Quantizer(scale, zero_point, min_q, max_q, ch_axis, q_folded)

    def create_input_fn_quantizer(self, attrs: Dict[str, Any]) -> None:
        self.input_quantizer = FNQuantizer(attrs)

    def create_weight_fn_quantizer(self, attrs: Dict[str, Any]) -> None:
        self.weight_quantizer = FNQuantizer(attrs)

    def create_bias_fn_quantizer(self, attrs: Dict[str, Any]) -> None:
        self.bias_quantizer = FNQuantizer(attrs)

    def create_input_quantizer(
        self, quant_info: Union[Tuple[numpy.typing.NDArray[numpy.float32], numpy.typing.NDArray[Any],
                                      numpy.typing.NDArray[Any], numpy.typing.NDArray[Any], int, bool], Dict[str, Any],
                                None]
    ) -> None:
        if isinstance(quant_info, dict):
            self.create_input_fn_quantizer(quant_info)
        elif isinstance(quant_info, tuple):
            self.create_input_qdq_quantizer(torch.from_numpy(quant_info[0]), torch.from_numpy(quant_info[1]),
                                            torch.from_numpy(quant_info[2]), torch.from_numpy(quant_info[3]),
                                            quant_info[4], quant_info[5])
        else:
            raise ValueError("Invalid quantization info: {}".format(quant_info))

    def create_weight_quantizer(
        self, quant_info: Union[Tuple[numpy.typing.NDArray[numpy.float32], numpy.typing.NDArray[Any],
                                      numpy.typing.NDArray[Any], numpy.typing.NDArray[Any], int, bool], Dict[str, Any],
                                None]
    ) -> None:
        if isinstance(quant_info, dict):
            self.create_weight_fn_quantizer(quant_info)
        elif isinstance(quant_info, tuple):
            self.create_weight_qdq_quantizer(torch.from_numpy(quant_info[0]), torch.from_numpy(quant_info[1]),
                                             torch.from_numpy(quant_info[2]), torch.from_numpy(quant_info[3]),
                                             quant_info[4], quant_info[5])
        else:
            raise ValueError("Invalid quantization info: {}".format(quant_info))

    def create_bias_quantizer(
        self, quant_info: Union[Tuple[numpy.typing.NDArray[numpy.float32], numpy.typing.NDArray[Any],
                                      numpy.typing.NDArray[Any], numpy.typing.NDArray[Any], int, bool], Dict[str, Any],
                                None]
    ) -> None:
        if isinstance(quant_info, dict):
            self.create_bias_fn_quantizer(quant_info)
        elif isinstance(quant_info, tuple):
            self.create_bias_qdq_quantizer(torch.from_numpy(quant_info[0]), torch.from_numpy(quant_info[1]),
                                           torch.from_numpy(quant_info[2]), torch.from_numpy(quant_info[3]),
                                           quant_info[4], quant_info[5])
        else:
            raise ValueError("Invalid quantization info: {}".format(quant_info))

    @abstractmethod
    def forward_impl(self, input: torch.Tensor, weight: torch.Tensor) -> torch.Tensor:
        pass

    def forward(self, input: torch.Tensor, output_size: Optional[List[int]] = None) -> torch.Tensor:
        if self.input_quantizer is not None:
            tensor = self.input_quantizer(input)
        else:
            tensor = input

        if self.weight_quantizer is not None:
            weight = self.weight_quantizer(self.weight)
        else:
            weight = self.weight.data

        weight = weight * self.w_alpha

        output = self.forward_impl(tensor, weight)

        if self.bias is not None:
            if self.bias_quantizer is not None:
                bias = self.bias_quantizer(self.bias)
            else:
                bias = self.bias.data

            bias = bias * self.b_beta

            # The bias is always 1D tensor (vector). If the output is not 1D,
            # should expand the dims of bias for broadcasting
            if output.dim() >= 2:
                bias = bias.view(1, -1, *([1] * (output.dim() - 2)))

            output = output + bias

        return output
