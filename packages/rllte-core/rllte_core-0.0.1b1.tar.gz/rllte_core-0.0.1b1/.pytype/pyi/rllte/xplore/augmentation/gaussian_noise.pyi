# (generated with --quick)

import rllte.common.base_augmentation
import torch as th
from typing import Any, Type

BaseAugmentation: Type[rllte.common.base_augmentation.BaseAugmentation]
Normal: Any

class GaussianNoise(rllte.common.base_augmentation.BaseAugmentation):
    __doc__: str
    dist: Any
    def __init__(self, mu: float = ..., sigma: float = ...) -> None: ...
    def forward(self, x) -> Any: ...
