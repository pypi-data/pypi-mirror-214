# (generated with --quick)

import os
import pathlib
import rllte.common.policies.on_policy_shared_actor_critic
import rllte.common.utils
import torch as th
from torch import nn
from torch.nn import functional as F
from typing import Any, Type, Union

BoxActor: Type[rllte.common.policies.on_policy_shared_actor_critic.BoxActor]
DiscreteActor: Type[rllte.common.policies.on_policy_shared_actor_critic.DiscreteActor]
ExportModel: Type[rllte.common.utils.ExportModel]
MultiBinaryActor: Type[rllte.common.policies.on_policy_shared_actor_critic.MultiBinaryActor]
Path: Type[pathlib.Path]

class OnPolicyDecoupledActorCritic(Any):
    __doc__: str
    action_dim: int
    action_type: str
    actor: Union[rllte.common.policies.on_policy_shared_actor_critic.BoxActor, rllte.common.policies.on_policy_shared_actor_critic.DiscreteActor, rllte.common.policies.on_policy_shared_actor_critic.MultiBinaryActor]
    actor_encoder: None
    critic: Any
    critic_encoder: None
    dist: None
    gae: Any
    def __init__(self, obs_shape: tuple, action_dim: int, action_type: str, feature_dim: int, hidden_dim: int) -> None: ...
    def evaluate_actions(self, obs, actions = ...) -> tuple: ...
    def get_action_and_value(self, obs, training: bool = ...) -> Any: ...
    def get_value(self, obs) -> Any: ...
    def load(self, path: str) -> None: ...
    def save(self, path: pathlib.Path, pretraining: bool = ...) -> None: ...
