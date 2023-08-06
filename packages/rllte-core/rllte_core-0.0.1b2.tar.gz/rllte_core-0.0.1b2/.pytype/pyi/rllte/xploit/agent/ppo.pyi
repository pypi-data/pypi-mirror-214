# (generated with --quick)

import gymnasium as gym
import numpy as np
import rllte.xploit.agent.on_policy_agent
import torch as th
from torch import nn
from typing import Any, Callable, Dict, Type

OnPolicyAgent: Type[rllte.xploit.agent.on_policy_agent.OnPolicyAgent]

class PPO(rllte.xploit.agent.on_policy_agent.OnPolicyAgent):
    __doc__: str
    aug_coef: float
    clip_range: float
    clip_range_vf: float
    ent_coef: float
    eps: float
    lr: float
    max_grad_norm: float
    n_epochs: int
    network_init_method: str
    opt: Any
    vf_coef: float
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., pretraining: bool = ..., num_steps: int = ..., eval_every_episodes: int = ..., feature_dim: int = ..., batch_size: int = ..., lr: float = ..., eps: float = ..., hidden_dim: int = ..., clip_range: float = ..., clip_range_vf: float = ..., n_epochs: int = ..., vf_coef: float = ..., ent_coef: float = ..., aug_coef: float = ..., max_grad_norm: float = ..., network_init_method: str = ...) -> None: ...
    def freeze(self) -> None: ...
    def update(self) -> Dict[str, float]: ...

def get_network_init(method: str = ...) -> Callable: ...
