#


## RandomCutout
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/augmentation/random_cutout.py/#L31)
```python 
RandomCutout(
   min_cut: int = 10, max_cut: int = 30
)
```


---
Random Cutout operation for image augmentation.


**Args**

* **min_cut** (int) : Min size of the cut shape.
* **max_cut** (int) : Max size of the cut shape.


**Returns**

Augmented images.


**Methods:**


### .forward
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/augmentation/random_cutout.py/#L47)
```python
.forward(
   x: th.Tensor
)
```

