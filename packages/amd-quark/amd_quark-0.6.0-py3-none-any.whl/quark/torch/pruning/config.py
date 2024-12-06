#
# Copyright (C) 2024, Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
"""Quark Pruning Config API for PyTorch"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass(eq=True)
class Config:
    """
    A class that encapsulates comprehensive pruning configurations for a machine learning model, allowing for detailed and hierarchical control over pruning parameters across different model components.

    :param Optional[AlgoConfig] algo_config: Optional configuration for the pruning algorithm, such as OSSCAR. After this process, the params will be reduced. Default is None.
    :param Optional[int] log_severity_level: 0:DEBUG, 1:INFO, 2:WARNING. 3:ERROR, 4:CRITICAL/FATAL. Default is 1.
    """
    # Optional configuration for the pruning algorithm, such as OSSCAR
    # After this process, the datatype/fake_datatype of weights will be changed with pruning scales.
    algo_config: Optional[AlgoConfig] = None

    # Log level for printing on screen
    log_severity_level: Optional[int] = 1


@dataclass
class AlgoConfig:
    name: str = ""

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {"name": self.name if self.name != "" else None}


@dataclass
class OSSCARConfig(AlgoConfig):

    name: str = "osscar"
    damp_percent: float = 0.01
    true_sequential: bool = True
    inside_layer_modules: Optional[List[str]] = None
    mlp_pruning_modules: Optional[List[str]] = None
    mlp_scaling_layers: Optional[Dict[str, Optional[str]]] = None
    mlp_pruning_ratio: float = 0.1
    mlp_intermediate_size_name: Optional[str] = None
    model_decoder_layers: Optional[str] = None
