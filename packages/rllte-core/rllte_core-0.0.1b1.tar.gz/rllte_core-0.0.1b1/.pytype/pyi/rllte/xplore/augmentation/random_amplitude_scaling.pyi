# (generated with --quick)

import rllte.common.base_augmentation
import torch as th
from typing import Any, Type

BaseAugmentation: Type[rllte.common.base_augmentation.BaseAugmentation]
Uniform: Any

class RandomAmplitudeScaling(rllte.common.base_augmentation.BaseAugmentation):
    __doc__: str
    dist: Any
    def __init__(self, low: float = ..., high: float = ...) -> None: ...
    def forward(self, x) -> Any: ...
