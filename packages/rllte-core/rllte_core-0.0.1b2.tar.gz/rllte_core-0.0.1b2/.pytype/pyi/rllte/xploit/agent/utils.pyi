# (generated with --quick)

import numpy as np
import torch as th
from torch import nn
from typing import Tuple

def soft_update_params(net, target_net, tau: float) -> None: ...
def to_torch(xs: Tuple[np.ndarray, ...], device) -> tuple: ...
