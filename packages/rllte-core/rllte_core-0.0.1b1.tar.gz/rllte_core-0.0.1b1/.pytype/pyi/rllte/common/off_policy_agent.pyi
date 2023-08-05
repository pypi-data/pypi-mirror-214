# (generated with --quick)

import gymnasium as gym
import pathlib
import rllte.common.base_agent
import rllte.common.policies.off_policy_deterministic_actor_double_critic
import rllte.common.policies.off_policy_stochastic_actor_double_critic
import rllte.xploit.encoder.identity_encoder
import rllte.xploit.encoder.tassa_cnn_encoder
import rllte.xploit.storage.nstep_replay_storage
import rllte.xploit.storage.vanilla_replay_storage
import rllte.xplore.augmentation.identity
import rllte.xplore.augmentation.random_shift
import rllte.xplore.distribution.squashed_normal
import rllte.xplore.distribution.truncated_normal_noise
import torch as th
from rllte.common import utils
from typing import Any, Dict, Optional, Type, Union

BaseAgent: Type[rllte.common.base_agent.BaseAgent]
Identity: Type[rllte.xplore.augmentation.identity.Identity]
IdentityEncoder: Type[rllte.xploit.encoder.identity_encoder.IdentityEncoder]
NStepReplayStorage: Type[rllte.xploit.storage.nstep_replay_storage.NStepReplayStorage]
OffPolicyDeterministicActorDoubleCritic: Type[rllte.common.policies.off_policy_deterministic_actor_double_critic.OffPolicyDeterministicActorDoubleCritic]
OffPolicyStochasticActorDoubleCritic: Type[rllte.common.policies.off_policy_stochastic_actor_double_critic.OffPolicyStochasticActorDoubleCritic]
Path: Type[pathlib.Path]
RandomShift: Type[rllte.xplore.augmentation.random_shift.RandomShift]
SquashedNormal: Type[rllte.xplore.distribution.squashed_normal.SquashedNormal]
TassaCnnEncoder: Type[rllte.xploit.encoder.tassa_cnn_encoder.TassaCnnEncoder]
TruncatedNormalNoise: Type[rllte.xplore.distribution.truncated_normal_noise.TruncatedNormalNoise]
VanillaReplayStorage: Type[rllte.xploit.storage.vanilla_replay_storage.VanillaReplayStorage]

class OffPolicyAgent(rllte.common.base_agent.BaseAgent):
    __doc__: str
    aug: Any
    dist: Union[rllte.xplore.distribution.truncated_normal_noise.TruncatedNormalNoise, Type[rllte.xplore.distribution.squashed_normal.SquashedNormal]]
    encoder: Union[rllte.xploit.encoder.identity_encoder.IdentityEncoder, rllte.xploit.encoder.tassa_cnn_encoder.TassaCnnEncoder]
    eval_every_steps: int
    feature_dim: Any
    global_episode: int
    global_step: int
    num_init_steps: int
    policy: Union[rllte.common.policies.off_policy_deterministic_actor_double_critic.OffPolicyDeterministicActorDoubleCritic, rllte.common.policies.off_policy_stochastic_actor_double_critic.OffPolicyStochasticActorDoubleCritic]
    storage: Union[rllte.xploit.storage.nstep_replay_storage.NStepReplayStorage, rllte.xploit.storage.vanilla_replay_storage.VanillaReplayStorage]
    training: bool
    def __init__(self, env, eval_env = ..., tag: str = ..., seed: int = ..., device: str = ..., pretraining: bool = ..., num_init_steps: int = ..., eval_every_steps: int = ..., **kwargs) -> None: ...
    def eval(self) -> Dict[str, float]: ...
    def freeze(self) -> None: ...
    def mode(self, training: bool = ...) -> None: ...
    def train(self, num_train_steps: int = ..., init_model_path: Optional[str] = ...) -> None: ...
    def update(self) -> Dict[str, float]: ...
