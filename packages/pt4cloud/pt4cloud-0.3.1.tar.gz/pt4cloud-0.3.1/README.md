# PT4Cloud

PT4Cloud (Performance Testing for Cloud) is a Python implementation of the performance testing methodology described by He et al. in their paper ["Performance Testing for Cloud Applications: A Systematic Approach"](https://doi.org/10.1145/3338906.3338912) (AST 2019). This project is not affiliated with the researchers.

## Overview

This package implements the PT4Cloud methodology for determining when cloud application performance characteristics have stabilized. It offers two variants:
- `pt4cloud`: Implements the full methodology as described in the paper (currently broken)
- `pt4cloud_lite`: A modified version for shorter testing intervals

The methodology uses statistical techniques to determine when a cloud application's performance distribution has stabilized, accounting for the inherent variability in cloud environments.

## Installation

```bash
pip install pt4cloud
```

## Quick Start

```python
from pt4cloud import pt4cloud, pt4cloud_lite
import random

# Example benchmark function that simulates latency measurements
def benchmark_function():
    # Simulate some workload with variable latency
    return random.normalvariate(100, 15)  # mean=100ms, std=15ms

# For short-term analysis (< 7 days)
samples, distribution = pt4cloud_lite(
    benchmark_function,
    stability_probability=0.9,    # 90% confidence level
    interval_duration=3600,      # 1 hour intervals
    sampling_portion=0.5         # Sample 50% of the time
)
```

## Methodology

The implemented approach follows the process described by He et al.:

1. **Data Collection**: Continuously execute performance tests over specified time intervals
2. **Distribution Analysis**: Calculate performance distributions using Kernel Density Estimation
3. **Stability Detection**: Compare successive distributions using Kullback-Leibler divergence
4. **Iteration**: Continue testing until stability is achieved or maximum iterations reached

The methodology addresses key challenges in cloud performance testing:
- Temporal variations in performance
- Non-normal performance distributions
- Need for statistical stability before drawing conclusions

## Detailed Usage

### PT4Cloud Lite (Short-term Analysis)

Modified version for shorter testing intervals:

```python
from pt4cloud import pt4cloud_lite

samples = pt4cloud_lite(
    benchmark_function=my_benchmark,
    stability_probability=0.9,    # 90% confidence level
    max_intervals=10,            # Maximum number of intervals to try
    interval_duration=86400,     # Duration of each interval in seconds (24 hours)
    interval_increase=0.2,       # Factor to increase interval duration by after each failed attempt
    sampling_portion=1.0,        # Fraction of time to spend sampling
    validate=True                # Whether to validate stability with additional interval
)
```

### Analyzing Results

```python
import numpy as np

# Get basic statistics
mean = np.mean(samples)
std = np.std(samples)
percentile_95 = np.percentile(samples, 95)

# Evaluate the probability density at specific points
x_points = np.linspace(min(samples), max(samples), 100)
density = distribution(x_points)
```

## Requirements

- Python 3.8+
- NumPy
- SciPy

## License

This work is licensed under the Creative Commons Attribution 4.0 International License. (https://creativecommons.org/licenses/by/4.0/)

