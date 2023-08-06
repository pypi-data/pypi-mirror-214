# (generated with --quick)

import rllte.common.base_augmentation
import torch as th
from typing import Any, Type

BaseAugmentation: Type[rllte.common.base_augmentation.BaseAugmentation]

class RandomTranslate(rllte.common.base_augmentation.BaseAugmentation):
    __doc__: str
    scale_factor: float
    size: int
    def __init__(self, size: int = ..., scale_factor: float = ...) -> None: ...
    def forward(self, x) -> Any: ...
