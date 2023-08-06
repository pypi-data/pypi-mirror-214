# (generated with --quick)

import os
import pathlib
import rllte.common.utils
import torch as th
from torch import nn
from typing import Any, Tuple, Type

Distribution: Any
ExportModel: Type[rllte.common.utils.ExportModel]
Path: Type[pathlib.Path]

class DoubleCritic(Any):
    Q1: Any
    Q2: Any
    __doc__: str
    def __init__(self, action_dim: int, feature_dim: int = ..., hidden_dim: int = ...) -> None: ...
    def forward(self, obs, action) -> tuple: ...

class OffPolicyDeterministicActorDoubleCritic(Any):
    __doc__: str
    actor: Any
    critic: DoubleCritic
    critic_target: DoubleCritic
    dist: None
    encoder: None
    def __init__(self, action_dim: int, feature_dim: int = ..., hidden_dim: int = ...) -> None: ...
    def forward(self, obs, training: bool = ..., step: int = ...) -> Tuple[Any]: ...
    def get_dist(self, obs, step: int) -> Any: ...
    def load(self, path: str) -> None: ...
    def save(self, path: pathlib.Path, pretraining: bool = ...) -> None: ...
