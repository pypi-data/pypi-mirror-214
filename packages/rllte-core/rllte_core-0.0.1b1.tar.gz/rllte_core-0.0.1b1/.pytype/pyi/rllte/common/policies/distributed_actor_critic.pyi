# (generated with --quick)

import os
import pathlib
import rllte.common.utils
import torch as th
from torch import nn
from torch.nn import functional as F
from typing import Any, Dict, Tuple, Type, Union

Distribution: Any
ExportModel: Type[rllte.common.utils.ExportModel]
Path: Type[pathlib.Path]

class BoxActor(Any):
    __doc__: str
    actor_logstd: Any
    actor_mu: Any
    def __init__(self, obs_shape: tuple, action_dim: int, feature_dim: int, hidden_dim: int) -> None: ...
    def forward(self, obs) -> Any: ...
    def get_policy_outputs(self, obs) -> Tuple[Any, Any]: ...

class DiscreteActor(Any):
    __doc__: str
    actor: Any
    def __init__(self, obs_shape: tuple, action_dim: int, feature_dim: int, hidden_dim: int) -> None: ...
    def forward(self, obs) -> Any: ...
    def get_policy_outputs(self, obs) -> Tuple[Any]: ...

class DistributedActorCritic(Any):
    __doc__: str
    action_dim: int
    action_range: list
    action_shape: tuple
    action_type: str
    actor: Union[BoxActor, DiscreteActor]
    critic: Any
    dist: None
    encoder: None
    lstm: Any
    policy_reshape_dim: int
    use_lstm: bool
    def __init__(self, obs_shape: tuple, action_shape: tuple, action_dim: int, action_type: str, action_range: list, feature_dim: int, hidden_dim: int = ..., use_lstm: bool = ...) -> None: ...
    def forward(self, inputs: dict, lstm_state: tuple = ...) -> Any: ...
    def get_action(self, inputs: Dict[str, Any], lstm_state: tuple = ..., training: bool = ...) -> Tuple[Dict[str, Any], tuple]: ...
    def get_dist(self, outputs) -> Any: ...
    def init_state(self, batch_size: int) -> tuple: ...
    def load(self, path: str) -> None: ...
    def save(self, path: pathlib.Path) -> None: ...
