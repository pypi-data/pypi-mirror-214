# (generated with --quick)

import os
import pathlib
import rllte.common.utils
import torch as th
from torch import nn
from typing import Any, Dict, Optional, Tuple, Type, TypeVar, Union

ExportModel: Type[rllte.common.utils.ExportModel]
Path: Type[pathlib.Path]

_T = TypeVar('_T')

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

class MultiBinaryActor(Any):
    __doc__: str
    actor: Any
    def __init__(self, obs_shape: tuple, action_dim: int, feature_dim: int, hidden_dim: int) -> None: ...
    def forward(self, obs) -> Any: ...
    def get_policy_outputs(self, obs) -> Tuple[Any]: ...

class OnPolicySharedActorCritic(Any):
    __doc__: str
    actor: Union[BoxActor, DiscreteActor, MultiBinaryActor]
    aux_critic: Any
    critic: Any
    dist: None
    encoder: None
    def __init__(self, obs_shape: tuple, action_dim: int, action_type: str, feature_dim: int, hidden_dim: int, aux_critic: bool = ...) -> None: ...
    def evaluate_actions(self, obs, actions = ...) -> tuple: ...
    def get_action_and_value(self, obs, training: bool = ...) -> Any: ...
    def get_dist_and_aux_value(self, obs) -> tuple: ...
    def get_policy_outputs(self, obs) -> Any: ...
    def get_value(self, obs) -> Any: ...
    def load(self, path: str) -> None: ...
    def save(self, path: pathlib.Path, pretraining: bool = ...) -> None: ...

def deepcopy(x: _T, memo: Optional[Dict[int, Any]] = ..., _nil = ...) -> _T: ...
