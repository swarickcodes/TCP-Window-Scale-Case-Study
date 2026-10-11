# Adaptive TCP Window Scaling Engine (RFC 7323)

A Python implementation of an adaptive transport layer flow control engine for high Bandwidth-Delay Product (BDP) networks.

## Features
- **Dynamic BDP Solver**: Dynamically calculates the shift exponent S = ceil(log2(BDP / 65535)).
- **Binary Option Parser**: Direct byte-level encoding/decoding of TCP Option Kind 3.
- **Edge Guards**: Implements Right-Edge Monotonicity checks and middlebox fallback (S = 0).

## How to Run
- Run test scenarios: `python transmission_simulator.py`
- Generate comparison chart: `python benchmark_visualizer.py`