# (generated with --quick)

import argparse
import rllte.xploit.agent.ppo
import rllte.xploit.encoder.espeholt_residual_encoder
from typing import Any, Type

EspeholtResidualEncoder: Type[rllte.xploit.encoder.espeholt_residual_encoder.EspeholtResidualEncoder]
PPO: Type[rllte.xploit.agent.ppo.PPO]
agent: rllte.xploit.agent.ppo.PPO
args: argparse.Namespace
encoder: rllte.xploit.encoder.espeholt_residual_encoder.EspeholtResidualEncoder
env: Any
eval_env: Any
feature_dim: int
parser: argparse.ArgumentParser

def make_procgen_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., gamma: float = ..., num_levels: int = ..., start_level: int = ..., distribution_mode: str = ...) -> Any: ...
