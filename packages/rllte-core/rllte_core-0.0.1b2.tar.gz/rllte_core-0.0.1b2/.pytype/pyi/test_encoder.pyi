# (generated with --quick)

import pytest
import rllte.xploit.encoder.espeholt_residual_encoder
import rllte.xploit.encoder.identity_encoder
import rllte.xploit.encoder.mnih_cnn_encoder
import rllte.xploit.encoder.pathak_cnn_encoder
import rllte.xploit.encoder.tassa_cnn_encoder
import rllte.xploit.encoder.vanilla_mlp_encoder
import torch as th
from typing import Any, Type

EspeholtResidualEncoder: Type[rllte.xploit.encoder.espeholt_residual_encoder.EspeholtResidualEncoder]
IdentityEncoder: Type[rllte.xploit.encoder.identity_encoder.IdentityEncoder]
MnihCnnEncoder: Type[rllte.xploit.encoder.mnih_cnn_encoder.MnihCnnEncoder]
PathakCnnEncoder: Type[rllte.xploit.encoder.pathak_cnn_encoder.PathakCnnEncoder]
TassaCnnEncoder: Type[rllte.xploit.encoder.tassa_cnn_encoder.TassaCnnEncoder]
VanillaMlpEncoder: Type[rllte.xploit.encoder.vanilla_mlp_encoder.VanillaMlpEncoder]
test_encoder: Any

def make_dmc_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., visualize_reward: bool = ..., from_pixels: bool = ..., height: int = ..., width: int = ..., frame_stack: int = ..., action_repeat: int = ...) -> Any: ...
