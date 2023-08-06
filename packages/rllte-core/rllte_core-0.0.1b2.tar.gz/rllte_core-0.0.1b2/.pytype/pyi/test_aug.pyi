# (generated with --quick)

import pytest
import rllte.xplore.augmentation.gaussian_noise
import rllte.xplore.augmentation.grayscale
import rllte.xplore.augmentation.identity
import rllte.xplore.augmentation.random_amplitude_scaling
import rllte.xplore.augmentation.random_colorjitter
import rllte.xplore.augmentation.random_convolution
import rllte.xplore.augmentation.random_crop
import rllte.xplore.augmentation.random_cutout
import rllte.xplore.augmentation.random_cutoutcolor
import rllte.xplore.augmentation.random_flip
import rllte.xplore.augmentation.random_rotate
import rllte.xplore.augmentation.random_shift
import rllte.xplore.augmentation.random_translate
import torch as th
from typing import Any, Type

GaussianNoise: Type[rllte.xplore.augmentation.gaussian_noise.GaussianNoise]
GrayScale: Type[rllte.xplore.augmentation.grayscale.GrayScale]
Identity: Type[rllte.xplore.augmentation.identity.Identity]
RandomAmplitudeScaling: Type[rllte.xplore.augmentation.random_amplitude_scaling.RandomAmplitudeScaling]
RandomColorJitter: Type[rllte.xplore.augmentation.random_colorjitter.RandomColorJitter]
RandomConvolution: Type[rllte.xplore.augmentation.random_convolution.RandomConvolution]
RandomCrop: Type[rllte.xplore.augmentation.random_crop.RandomCrop]
RandomCutout: Type[rllte.xplore.augmentation.random_cutout.RandomCutout]
RandomCutoutColor: Type[rllte.xplore.augmentation.random_cutoutcolor.RandomCutoutColor]
RandomFlip: Type[rllte.xplore.augmentation.random_flip.RandomFlip]
RandomRotate: Type[rllte.xplore.augmentation.random_rotate.RandomRotate]
RandomShift: Type[rllte.xplore.augmentation.random_shift.RandomShift]
RandomTranslate: Type[rllte.xplore.augmentation.random_translate.RandomTranslate]
test_image_augmentation: Any
test_state_augmentation: Any

def make_dmc_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., visualize_reward: bool = ..., from_pixels: bool = ..., height: int = ..., width: int = ..., frame_stack: int = ..., action_repeat: int = ...) -> Any: ...
