# (generated with --quick)

import gymnasium as gym
import rllte.xploit.agent.off_policy_agent
import torch as th
from rllte.xploit.agent import utils
from torch.nn import functional as F
from typing import Any, Callable, Dict, Type

OffPolicyAgent: Type[rllte.xploit.agent.off_policy_agent.OffPolicyAgent]

class DrQv2(rllte.xploit.agent.off_policy_agent.OffPolicyAgent):
    __doc__: str
    actor_opt: Any
    critic_opt: Any
    critic_target_tau: float
    encoder_opt: Any
    eps: float
    lr: float
    network_init_method: str
    update_every_steps: int
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., pretraining: bool = ..., num_init_steps: int = ..., eval_every_steps: int = ..., feature_dim: int = ..., batch_size: int = ..., lr: float = ..., eps: float = ..., hidden_dim: int = ..., critic_target_tau: float = ..., update_every_steps: int = ..., network_init_method: str = ...) -> None: ...
    def freeze(self) -> None: ...
    def update(self) -> Dict[str, float]: ...
    def update_actor(self, obs) -> Dict[str, float]: ...
    def update_critic(self, obs, action, reward, discount, next_obs) -> Dict[str, float]: ...

def get_network_init(method: str = ...) -> Callable: ...
