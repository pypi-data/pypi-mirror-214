# (generated with --quick)

import gymnasium as gym
import os
import pathlib
import rllte.xploit.agent.distributed_agent
import threading
import torch as th
import traceback
from torch import multiprocessing as mp
from torch import nn
from torch.nn import functional as F
from typing import Any, Callable, Dict, Optional, Tuple, Type, TypeVar

DistributedAgent: Type[rllte.xploit.agent.distributed_agent.DistributedAgent]
Environment: Type[rllte.xploit.agent.distributed_agent.Environment]
Path: Type[pathlib.Path]

_T = TypeVar('_T')

class IMPALA(rllte.xploit.agent.distributed_agent.DistributedAgent):
    __doc__: str
    baseline_coef: float
    discount: float
    ent_coef: float
    eps: float
    feature_dim: int
    lr: float
    lr_scheduler: Any
    max_grad_norm: float
    network_init_method: str
    opt: Any
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., num_steps: int = ..., num_actors: int = ..., num_learners: int = ..., num_storages: int = ..., feature_dim: int = ..., batch_size: int = ..., lr: float = ..., eps: float = ..., use_lstm: bool = ..., ent_coef: float = ..., baseline_coef: float = ..., max_grad_norm: float = ..., discount: float = ..., network_init_method: str = ...) -> None: ...
    def act(self, env: rllte.xploit.agent.distributed_agent.Environment, actor_idx: int, free_queue, full_queue, init_actor_state_storages: list) -> None: ...
    def freeze(self) -> None: ...
    def load(self, path: str) -> None: ...
    def save(self) -> None: ...
    def update(self, batch: dict, init_actor_states: tuple, lock = ...) -> Dict[str, tuple]: ...

class VTraceLoss:
    __doc__: str
    clip_pg_rho_threshold: float
    clip_rho_threshold: float
    def __call__(self, batch) -> Tuple[Any, Any, Any]: ...
    def __init__(self, clip_rho_threshold: float = ..., clip_pg_rho_threshold: float = ...) -> None: ...
    def compute_ISW(self, target_dist, behavior_dist, action) -> Any: ...

def deepcopy(x: _T, memo: Optional[Dict[int, Any]] = ..., _nil = ...) -> _T: ...
def get_network_init(method: str = ...) -> Callable: ...
