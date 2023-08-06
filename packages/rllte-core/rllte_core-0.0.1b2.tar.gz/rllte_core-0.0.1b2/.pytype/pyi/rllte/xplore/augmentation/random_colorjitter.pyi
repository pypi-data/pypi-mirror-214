# (generated with --quick)

import rllte.common.base_augmentation
import torch as th
from typing import Any, Type

BaseAugmentation: Type[rllte.common.base_augmentation.BaseAugmentation]
ColorJitter: Any

class RandomColorJitter(rllte.common.base_augmentation.BaseAugmentation):
    __doc__: str
    color_jitter: Any
    def __init__(self, brightness: float = ..., contrast: float = ..., saturation: float = ..., hue: float = ...) -> None: ...
    def forward(self, x) -> Any: ...
