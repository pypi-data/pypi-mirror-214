#


## RandomTranslate
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/augmentation/random_translate.py/#L31)
```python 
RandomTranslate(
   size: int = 256, scale_factor: float = 0.75
)
```


---
Random translate operation for processing image-based observations.


**Args**

* **size** (int) : The scale size in translated images
* **scale_factor** (float) : The scale factor ratio in translated images. Should have 0.0 <= scale_factor <= 1.0


**Returns**

Augmented images.


**Methods:**


### .forward
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/augmentation/random_translate.py/#L47)
```python
.forward(
   x: th.Tensor
)
```

