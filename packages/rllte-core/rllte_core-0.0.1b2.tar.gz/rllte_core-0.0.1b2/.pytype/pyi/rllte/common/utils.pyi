# (generated with --quick)

import numpy as np
import torch as th
from torch import nn
from typing import Any, Callable, Tuple

class ExportModel(Any):
    __doc__: str
    actor: Any
    encoder: Any
    def __init__(self, encoder, actor) -> None: ...
    def forward(self, obs) -> Any: ...

class eval_mode:
    __doc__: str
    models: tuple
    prev_states: list
    def __enter__(self) -> None: ...
    def __exit__(self, *args) -> bool: ...
    def __init__(self, *models) -> None: ...

def get_network_init(method: str = ...) -> Callable: ...
def to_numpy(xs: tuple) -> Tuple[np.ndarray, ...]: ...
