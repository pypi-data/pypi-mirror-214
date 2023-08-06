# (generated with --quick)

import collections
import gymnasium as gym
import numpy as np
import os
import pathlib
import rllte.common.base_agent
import rllte.common.policies.distributed_actor_critic
import rllte.xploit.encoder.identity_encoder
import rllte.xploit.encoder.mnih_cnn_encoder
import rllte.xploit.storage.distributed_storage
import rllte.xplore.distribution.categorical
import rllte.xplore.distribution.diagonal_gaussian
import threading
import time
import torch as th
from torch import multiprocessing as mp
from typing import Any, Callable, Dict, Optional, Type, Union

BaseAgent: Type[rllte.common.base_agent.BaseAgent]
Categorical: Type[rllte.xplore.distribution.categorical.Categorical]
DiagonalGaussian: Type[rllte.xplore.distribution.diagonal_gaussian.DiagonalGaussian]
DistributedActorCritic: Type[rllte.common.policies.distributed_actor_critic.DistributedActorCritic]
IdentityEncoder: Type[rllte.xploit.encoder.identity_encoder.IdentityEncoder]
MnihCnnEncoder: Type[rllte.xploit.encoder.mnih_cnn_encoder.MnihCnnEncoder]
Path: Type[pathlib.Path]
Storage: Type[rllte.xploit.storage.distributed_storage.DistributedStorage]
deque: Type[collections.deque]

class DistributedAgent(rllte.common.base_agent.BaseAgent):
    __doc__: str
    actor: rllte.common.policies.distributed_actor_critic.DistributedActorCritic
    batch_size: Any
    dist: Type[Union[rllte.xplore.distribution.categorical.Categorical, rllte.xplore.distribution.diagonal_gaussian.DiagonalGaussian]]
    encoder: Union[rllte.xploit.encoder.identity_encoder.IdentityEncoder, rllte.xploit.encoder.mnih_cnn_encoder.MnihCnnEncoder]
    env: Any
    feature_dim: Any
    learner: rllte.common.policies.distributed_actor_critic.DistributedActorCritic
    lr_lambda: Callable[..., float]
    num_actors: int
    num_learners: int
    num_steps: int
    num_storages: int
    storage: rllte.xploit.storage.distributed_storage.DistributedStorage
    training: bool
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., num_steps: int = ..., num_actors: int = ..., num_learners: int = ..., num_storages: int = ..., **kwargs) -> None: ...
    def act(self) -> None: ...
    def eval(self) -> Dict[str, float]: ...
    def freeze(self) -> None: ...
    def mode(self, training: bool = ...) -> None: ...
    def train(self, num_train_steps: int = ..., init_model_path: Optional[str] = ...) -> None: ...
    def update(self) -> Dict[str, float]: ...

class Environment:
    __doc__: str
    action_dim: Any
    action_type: str
    env: Any
    episode_return: Any
    episode_step: Any
    def __init__(self, env) -> None: ...
    def _format_obs(self, obs: np.ndarray) -> Any: ...
    def close(self) -> None: ...
    def reset(self, seed) -> Dict[str, Any]: ...
    def step(self, action) -> Dict[str, Any]: ...
