# (generated with --quick)

import gymnasium as gym
import itertools
import numpy as np
import rllte.xploit.agent.on_policy_agent
import torch as th
from torch import nn
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union

OnPolicyAgent: Type[rllte.xploit.agent.on_policy_agent.OnPolicyAgent]

_T = TypeVar('_T')

class DAAC(rllte.xploit.agent.on_policy_agent.OnPolicyAgent):
    __doc__: str
    actor_opt: Any
    actor_params: itertools.chain
    adv_coef: float
    aug_coef: float
    clip_range: float
    clip_range_vf: float
    critic_opt: Any
    critic_params: itertools.chain
    ent_coef: float
    eps: float
    lr: float
    max_grad_norm: float
    network_init_method: str
    num_policy_updates: int
    policy_epochs: int
    prev_total_critic_loss: Union[int, list]
    value_epochs: int
    value_freq: int
    vf_coef: float
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., pretraining: bool = ..., num_steps: int = ..., eval_every_episodes: int = ..., feature_dim: int = ..., batch_size: int = ..., lr: float = ..., eps: float = ..., hidden_dim: int = ..., clip_range: float = ..., clip_range_vf: float = ..., policy_epochs: int = ..., value_freq: int = ..., value_epochs: int = ..., vf_coef: float = ..., ent_coef: float = ..., aug_coef: float = ..., adv_coef: float = ..., max_grad_norm: float = ..., network_init_method: str = ...) -> None: ...
    def freeze(self) -> None: ...
    def update(self) -> Dict[str, float]: ...

def deepcopy(x: _T, memo: Optional[Dict[int, Any]] = ..., _nil = ...) -> _T: ...
def get_network_init(method: str = ...) -> Callable: ...
