#
# Modifications copyright(c) 2023 Advanced Micro Devices,Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from __future__ import annotations

from typing import Optional, Tuple, Any, Dict, List

import numpy as np
import numpy.typing as npt
import onnx
from pathlib import Path

from onnx.onnx_pb import GraphProto, ModelProto, NodeProto, TensorProto

from onnxruntime.capi._pybind_state import quantize_matmul_4bits

from onnxruntime.quantization.onnx_model import ONNXModel
from onnxruntime.quantization.quant_utils import attribute_to_kwarg

from quark.shares.utils.log import ScreenLogger

logger = ScreenLogger(__name__)


class WeightOnlyQuantConfig:

    def __init__(self, algorithm: str) -> None:
        """This is the Base class for Weight Only Quant Configuration.

        Args:
            algorithm:
                weight only quantize algorithm name.
        """
        self.algorithm = algorithm


class DefaultWeightOnlyQuantConfig(WeightOnlyQuantConfig):

    def __init__(
        self,
        block_size: int = 128,
        is_symmetric: bool = False,
        bits: int = 4,
        accuracy_level: int | None = None,
    ):
        super().__init__(algorithm="DEFAULT")
        self.block_size = block_size
        self.is_symmetric = is_symmetric
        self.bits = bits
        self.accuracy_level = accuracy_level


class GPTQWeightOnlyQuantConfig(WeightOnlyQuantConfig):

    def __init__(
            self,
            calibration_data_reader: torch.utils.data.DataLoader,  # type: ignore
            percdamp: float = 0.01,
            block_size: int = 128,
            actorder: bool = False,
            mse: bool = False,
            perchannel: bool = True):
        super().__init__(algorithm="GPTQ")
        self.calibration_data_reader = calibration_data_reader
        self.percdamp = percdamp
        self.block_size = block_size

        self.actorder = actorder
        self.mse = mse
        self.perchannel = perchannel


def get_onnx_initializer(name: str, graph_path: list[GraphProto]) -> Tuple[Optional[TensorProto], Any]:
    for gid in range(len(graph_path) - 1, -1, -1):
        graph = graph_path[gid]
        for tensor in graph.initializer:
            if tensor.name == name:
                return tensor, graph
    return None, None


class DefaultWeightOnlyQuantizer:

    def __init__(self, config: DefaultWeightOnlyQuantConfig):
        self.config = config

    def int4_block_quant(
            self, fp32weight: Any) -> Tuple[npt.NDArray[np.uint8], npt.NDArray[np.float32], npt.NDArray[np.uint8]]:
        """4b quantize fp32 weight to a blob"""

        if len(fp32weight.shape) != 2:
            raise ValueError("Current int4 block quantization only supports 2D tensors!")
        rows, cols = fp32weight.shape
        block_size = self.config.block_size
        blob_size = block_size // 2
        k_blocks = (rows + block_size - 1) // block_size
        padded_rows = k_blocks * block_size
        pad_len = padded_rows - rows
        if pad_len > 0:
            fp32weight = np.pad(fp32weight, ((0, pad_len), (0, 0)), "constant")

        # block wise quantization, each block comes from a single column
        packed = np.zeros((cols, k_blocks, blob_size), dtype="uint8")
        scales = np.zeros((cols * k_blocks), dtype=fp32weight.dtype)
        zero_point = np.zeros(cols * ((k_blocks + 1) // 2), dtype="uint8")
        quantize_matmul_4bits(packed, fp32weight, scales, zero_point, block_size, cols, rows, self.config.is_symmetric)

        return (packed, scales, zero_point)

    def quantize(self, node: NodeProto, graph_stack: list[GraphProto]) -> NodeProto:
        """If the node is MatMul with fp32 const weight, quantize the weight with int4, and return the new node"""

        if node.op_type != "MatMul":
            return node  # only care about MatMul for now

        logger.info(f"start to quantize {node.name} ...")
        inputB = node.input[1]  # noqa: N806
        B, Bs_graph = get_onnx_initializer(inputB, graph_stack)  # noqa: N806
        if B is None:
            logger.info("MatMul doesn't have const weight. Skip to quantize")
            return node  # only care about constant weight

        B_array = onnx.numpy_helper.to_array(B)  # noqa: N806
        if len(B_array.shape) != 2:
            logger.info("MatMul weight is not 2D. Skip to quantize")
            return node  # can only process 2-D matrix

        packed, scales, zero_points = self.int4_block_quant(B_array)
        B_quant = onnx.numpy_helper.from_array(packed)  # noqa: N806
        B_quant.name = B.name + "_Q4"
        for input_ in Bs_graph.input:
            if input_.name == inputB:
                Bs_graph.input.remove(input_)
                break

        scales_tensor = onnx.numpy_helper.from_array(scales)
        scales_tensor.name = B.name + "_scales"
        Bs_graph.initializer.extend([B_quant, scales_tensor])

        input_names = [node.input[0], B_quant.name, scales_tensor.name]
        if not self.config.is_symmetric:
            zp_tensor = onnx.numpy_helper.from_array(zero_points)
            zp_tensor.name = B.name + "_zero_points"
            Bs_graph.initializer.extend([zp_tensor])
            input_names.append(zp_tensor.name)

        kwargs: Dict[str, Any] = {}
        rows, cols = B_array.shape
        kwargs["K"] = rows
        kwargs["N"] = cols
        kwargs["bits"] = self.config.bits
        kwargs["block_size"] = self.config.block_size
        if self.config.accuracy_level is not None:
            kwargs["accuracy_level"] = self.config.accuracy_level

        matmul_q4_node = onnx.helper.make_node(
            "MatMulNBits",
            inputs=input_names,
            outputs=[node.output[0]],
            name=node.name + "_Q4" if node.name else "",
            domain="com.microsoft",
            **kwargs,
        )

        logger.info(f"complete quantization of {node.name} ...")

        return matmul_q4_node


class MatMulNBitsQuantizer:
    """Perform 4b quantization of constant MatMul weights"""

    def __init__(self,
                 model: ModelProto | str,
                 block_size: int = 128,
                 is_symmetric: bool = False,
                 bits: int = 4,
                 accuracy_level: int | None = None,
                 nodes_to_exclude: Optional[List[str]] = None,
                 algo_config: Optional[WeightOnlyQuantConfig] = None,
                 extra_options: Dict[str, Any] = {}):
        if nodes_to_exclude is None:
            nodes_to_exclude = []
        self.model = ONNXModel(onnx.load(model)) if isinstance(model, str) else ONNXModel(model)
        self.model_gptq = onnx.load(model) if isinstance(model, str) else model
        self.model_path = model if isinstance(model, str) else None
        self.block_size = block_size
        self.is_symmetric = is_symmetric
        self.accuracy_level = accuracy_level
        self.nodes_to_exclude = set(nodes_to_exclude)
        if algo_config is None:
            algo_config = DefaultWeightOnlyQuantConfig(block_size=block_size,
                                                       is_symmetric=is_symmetric,
                                                       bits=bits,
                                                       accuracy_level=accuracy_level)
        self.algo_config = algo_config
        if self.algo_config.algorithm in ["DEFAULT"]:
            self.node_quantizer = DefaultWeightOnlyQuantizer(self.algo_config)  # type: ignore
        self.extra_options = extra_options

    def _process_subgraph(self, graph_stack: list[GraphProto]) -> GraphProto:
        new_nodes = []
        graph = graph_stack[-1]

        for node in graph.node:
            # TODO: The support of subgraph need to be verified.
            graph_attrs = [
                attr for attr in node.attribute
                if attr.type == onnx.AttributeProto.GRAPH or attr.type == onnx.AttributeProto.GRAPHS
            ]
            if len(graph_attrs):
                kwargs = {}
                for attr in node.attribute:
                    if attr.type == onnx.AttributeProto.GRAPH:
                        # recursive call to take care of sub-graph
                        graph_stack.append(attr.g)
                        kv: Any = {attr.name: self._process_subgraph(graph_stack)}
                    elif attr.type == onnx.AttributeProto.GRAPHS:
                        value = []
                        for subgraph in attr.graphs:
                            # recursive call to take care of sub-graph
                            graph_stack.append(subgraph)
                            value.extend([self._process_subgraph(graph_stack)])
                        kv = {attr.name: value}
                    else:
                        kv = attribute_to_kwarg(attr)
                    kwargs.update(kv)
                node = onnx.helper.make_node(  # noqa: PLW2901
                    node.op_type, node.input, node.output, name=node.name, **kwargs)
            out_node = None
            if node.name in self.nodes_to_exclude:
                logger.info(f"exclude to quantize {node.name} as specified by nodes_to_exclude...")
                out_node = node
            else:
                out_node = self.node_quantizer.quantize(node, graph_stack)
            new_nodes.append(out_node)

        graph.ClearField("node")
        graph.node.extend(new_nodes)
        graph_stack.pop()
        return graph

    def quantize_model(self) -> None:
        if self.algo_config.algorithm in ["DEFAULT"]:
            # use a stack to keep track of sub-graphs
            graph_stack = [self.model.graph()]
            opset_import = self.model.opset_import()

            has_ms_domain = False
            for opset in opset_import:
                if opset.domain == "com.microsoft":
                    has_ms_domain = True
            if not has_ms_domain:
                opset_import.extend([onnx.helper.make_opsetid("com.microsoft", 1)])
            self._process_subgraph(graph_stack)
            self.model.clean_initializers()
        elif self.algo_config.algorithm in ["GPTQ"]:
            from quark.onnx.gptq.gptq import GptqProcessor
            import tempfile
            gptq_path = tempfile.TemporaryDirectory(prefix="vai.quant.")
            gptq_model_output = Path(gptq_path.name).joinpath("gptq_model.onnx").as_posix()
            gptq_processor = GptqProcessor(
                gptq_model_output,
                self.model_gptq,
                self.model_gptq,
                self.algo_config.calibration_data_reader,  # type: ignore[attr-defined]
                self.extra_options)
            self.model = gptq_processor.apply_matmul4bits()
