# (generated with --quick)

import abc
import datetime as _datetime
import gymnasium as gym
import numpy as np
import os
import pathlib
import pynvml
import random
import rllte.common.base_augmentation
import rllte.common.base_distribution
import rllte.common.base_encoder
import rllte.common.base_reward
import rllte.common.base_storage
import rllte.common.logger
import rllte.common.timer
import torch as th
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

ABC: Type[abc.ABC]
Augmentation: Type[rllte.common.base_augmentation.BaseAugmentation]
Distribution: Type[rllte.common.base_distribution.BaseDistribution]
Encoder: Type[rllte.common.base_encoder.BaseEncoder]
IntrinsicRewardModule: Type[rllte.common.base_reward.BaseIntrinsicRewardModule]
Logger: Type[rllte.common.logger.Logger]
Path: Type[pathlib.Path]
Storage: Type[rllte.common.base_storage.BaseStorage]
Timer: Type[rllte.common.timer.Timer]
datetime: Type[_datetime.datetime]
torch_npu: Any

_FuncT = TypeVar('_FuncT', bound=Callable)

class BaseAgent(abc.ABC):
    __doc__: str
    action_dim: Any
    action_range: List[Union[float, int]]
    action_shape: Any
    action_type: str
    aug: Any
    device: Any
    dist: Any
    encoder: Any
    env: Any
    eval_env: Any
    feature_dim: int
    global_episode: int
    global_step: int
    irs: Any
    logger: rllte.common.logger.Logger
    num_envs: Any
    num_eval_episodes: int
    obs_shape: Any
    pretraining: bool
    seed: int
    storage: Any
    timer: rllte.common.timer.Timer
    work_dir: pathlib.Path
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., pretraining: bool = ..., feature_dim: int = ...) -> None: ...
    def check(self) -> None: ...
    @abstractmethod
    def eval(self) -> Optional[Dict[str, float]]: ...
    @abstractmethod
    def freeze(self) -> None: ...
    def get_env_info(self, env) -> None: ...
    def get_npu_name(self) -> str: ...
    @abstractmethod
    def mode(self) -> None: ...
    def set(self, encoder = ..., storage = ..., distribution = ..., augmentation = ..., reward = ...) -> None: ...
    @abstractmethod
    def train(self) -> None: ...
    @abstractmethod
    def update(self) -> Dict[str, float]: ...

def abstractmethod(funcobj: _FuncT) -> _FuncT: ...
