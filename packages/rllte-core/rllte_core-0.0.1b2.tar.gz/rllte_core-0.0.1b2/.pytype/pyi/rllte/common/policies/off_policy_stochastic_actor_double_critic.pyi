# (generated with --quick)

import os
import pathlib
import rllte.common.policies.off_policy_deterministic_actor_double_critic
import rllte.common.utils
import torch as th
from torch import nn
from typing import Any, Tuple, Type

Distribution: Any
DoubleCritic: Type[rllte.common.policies.off_policy_deterministic_actor_double_critic.DoubleCritic]
ExportModel: Type[rllte.common.utils.ExportModel]
Path: Type[pathlib.Path]

class OffPolicyStochasticActorDoubleCritic(Any):
    __doc__: str
    actor: Any
    critic: rllte.common.policies.off_policy_deterministic_actor_double_critic.DoubleCritic
    critic_target: rllte.common.policies.off_policy_deterministic_actor_double_critic.DoubleCritic
    dist: None
    encoder: None
    log_std_max: Any
    log_std_min: Any
    def __init__(self, action_dim: int, feature_dim: int = ..., hidden_dim: int = ..., log_std_range: tuple = ...) -> None: ...
    def forward(self, obs, training: bool = ..., step: int = ...) -> Tuple[Any]: ...
    def get_dist(self, obs, step: int) -> Any: ...
    def load(self, path: str) -> None: ...
    def save(self, path: pathlib.Path, pretraining: bool = ...) -> None: ...
