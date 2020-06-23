Fast and stable solver for Kepler's equation extracted from [exoplanet](https://docs.exoplanet.codes).

## Installation

The best way to install is using pip:

```bash
python -m pip install kepler.py
```

## Usage

This package exposes two functions:

* `kepler`: Solves Kepler's equation and returns the cosine and sine of the true anomaly:

```python
import kepler
eccentric_anomaly, cos_true_anomaly, sin_true_anomaly = kepler.kepler(mean_anomaly, eccentricity)
```

* `solve`: A lower-level interface that is used by `kepler` to actually do the solving (*Note that this will return garbage for eccentricities out of the range zero to one*):

```python
import kepler
eccentric_anomaly = kepler.solve(mean_anomaly, eccentricity)
```
