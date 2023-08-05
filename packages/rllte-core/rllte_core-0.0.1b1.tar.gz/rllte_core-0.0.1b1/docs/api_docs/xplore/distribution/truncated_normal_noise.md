#


## TruncatedNormalNoise
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/distribution/truncated_normal_noise.py/#L34)
```python 
TruncatedNormalNoise(
   loc: float = 0.0, scale: float = 1.0, low: float = -1.0, high: float = 1.0,
   eps: float = 1e-06, stddev_schedule: str = 'linear(1.0, 0.1, 100000)',
   stddev_clip: float = 0.3
)
```


---
Truncated normal action noise. See Section 3.1 of
"Mastering Visual Continuous Control: Improved Data-Augmented Reinforcement Learning".


**Args**

* **loc** (float) : mean of the noise (often referred to as mu).
* **scale** (float) : standard deviation of the noise (often referred to as sigma).
* **low** (float) : The lower bound of the noise.
* **high** (float) : The upper bound of the noise.
* **eps** (float) : A small value to avoid numerical instability.
* **stddev_schedule** (str) : Use the exploration std schedule.
* **stddev_clip** (float) : The exploration std clip range.


**Returns**

Truncated normal noise instance.


**Methods:**


### .sample
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/distribution/truncated_normal_noise.py/#L80)
```python
.sample(
   clip: bool = False, sample_shape: th.Size = th.Size()
)
```

---
Generates a sample_shape shaped sample or sample_shape shaped batch of
samples if the distribution parameters are batched.


**Args**

* **clip** (bool) : Whether to perform noise truncation.
* **sample_shape** (th.Size) : The size of the sample to be drawn.


**Returns**

A sample_shape shaped sample.

### .rsample
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/distribution/truncated_normal_noise.py/#L101)
```python
.rsample(
   sample_shape: th.Size = th.Size()
)
```

---
Generates a sample_shape shaped sample or sample_shape shaped batch of
samples if the distribution parameters are batched.


**Args**

* **sample_shape** (th.Size) : The size of the sample to be drawn.


**Returns**

A sample_shape shaped sample.

### .log_prob
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/distribution/truncated_normal_noise.py/#L113)
```python
.log_prob(
   value: th.Tensor
)
```

---
Returns the log of the probability density/mass function evaluated at `value`.


**Args**

* **value** (th.Tensor) : The value to be evaluated.


**Returns**

The log_prob value.

### .reset
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/distribution/truncated_normal_noise.py/#L124)
```python
.reset(
   noiseless_action: th.Tensor, step: int = 0
)
```

---
Reset the noise instance.


**Args**

* **noiseless_action** (th.Tensor) : Unprocessed actions.
* **step** (int) : Global training step that can be None when there is no noise schedule.


**Returns**

None.

### .mean
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/distribution/truncated_normal_noise.py/#L140)
```python
.mean()
```

---
Returns the mean of the distribution.

### .mode
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/distribution/truncated_normal_noise.py/#L145)
```python
.mode()
```

---
Returns the mode of the distribution.

### .entropy
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/distribution/truncated_normal_noise.py/#L149)
```python
.entropy()
```

---
Returns the Shannon entropy of distribution.

### .stddev
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/distribution/truncated_normal_noise.py/#L154)
```python
.stddev()
```

---
Returns the standard deviation of the distribution.

### .variance
[source](https://github.com/RLE-Foundation/rllte/blob/main/rllte/xplore/distribution/truncated_normal_noise.py/#L159)
```python
.variance()
```

---
Returns the variance of the distribution.
