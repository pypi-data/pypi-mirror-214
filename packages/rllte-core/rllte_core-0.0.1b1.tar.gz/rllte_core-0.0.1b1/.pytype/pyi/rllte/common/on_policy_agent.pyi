# (generated with --quick)

import collections
import gymnasium as gym
import numpy as np
import pathlib
import rllte.common.base_agent
import rllte.common.policies.on_policy_decoupled_actor_critic
import rllte.common.policies.on_policy_shared_actor_critic
import rllte.xploit.encoder.identity_encoder
import rllte.xploit.encoder.pathak_cnn_encoder
import rllte.xploit.storage.vanilla_rollout_storage
import rllte.xplore.distribution.bernoulli
import rllte.xplore.distribution.categorical
import rllte.xplore.distribution.diagonal_gaussian
import torch as th
from rllte.common import utils
from typing import Any, Dict, Optional, Type, Union

BaseAgent: Type[rllte.common.base_agent.BaseAgent]
Bernoulli: Type[rllte.xplore.distribution.bernoulli.Bernoulli]
Categorical: Type[rllte.xplore.distribution.categorical.Categorical]
DiagonalGaussian: Type[rllte.xplore.distribution.diagonal_gaussian.DiagonalGaussian]
IdentityEncoder: Type[rllte.xploit.encoder.identity_encoder.IdentityEncoder]
OnPolicyDecoupledActorCritic: Type[rllte.common.policies.on_policy_decoupled_actor_critic.OnPolicyDecoupledActorCritic]
OnPolicySharedActorCritic: Type[rllte.common.policies.on_policy_shared_actor_critic.OnPolicySharedActorCritic]
Path: Type[pathlib.Path]
PathakCnnEncoder: Type[rllte.xploit.encoder.pathak_cnn_encoder.PathakCnnEncoder]
Storage: Type[rllte.xploit.storage.vanilla_rollout_storage.VanillaRolloutStorage]
deque: Type[collections.deque]

class OnPolicyAgent(rllte.common.base_agent.BaseAgent):
    __doc__: str
    dist: Type[Union[rllte.xplore.distribution.bernoulli.Bernoulli, rllte.xplore.distribution.categorical.Categorical, rllte.xplore.distribution.diagonal_gaussian.DiagonalGaussian]]
    encoder: Union[rllte.xploit.encoder.identity_encoder.IdentityEncoder, rllte.xploit.encoder.pathak_cnn_encoder.PathakCnnEncoder]
    eval_every_episodes: int
    feature_dim: Any
    global_episode: int
    global_step: Any
    num_steps: int
    policy: Union[rllte.common.policies.on_policy_decoupled_actor_critic.OnPolicyDecoupledActorCritic, rllte.common.policies.on_policy_shared_actor_critic.OnPolicySharedActorCritic]
    storage: rllte.xploit.storage.vanilla_rollout_storage.VanillaRolloutStorage
    training: bool
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., pretraining: bool = ..., num_steps: int = ..., eval_every_episodes: int = ..., shared_encoder: bool = ..., **kwargs) -> None: ...
    def eval(self) -> Dict[str, float]: ...
    def freeze(self) -> None: ...
    def mode(self, training: bool = ...) -> None: ...
    def train(self, num_train_steps: int = ..., init_model_path: Optional[str] = ...) -> None: ...
    def update(self) -> Dict[str, float]: ...
