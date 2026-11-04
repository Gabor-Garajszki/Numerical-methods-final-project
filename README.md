# Monte Carlo Option Pricing

## Features

* **Path Simulation:** Generates future asset price paths using Geometric Brownian Motion (GBM) via vectorized NumPy operations.
* **Option Pricing:** Calculates the expected payoff and discounted present value for European, Asian, and Barrier options.
* **The Greeks:** Computes risk management metrics (Delta, Gamma, Vega) using the bump-and-revalue (finite difference) method.
* **Modular Architecture:** Object-oriented design separating the market environment, simulation engine, and option contracts.
* **Validation:** Includes mathematical validation against standard Black-Scholes pricing models.

## Project Structure

```text
mc_option_pricing/
├── src/
│   ├── __init__.py
│   ├── market.py             # Market parameters (S0, r, vol, T)
│   ├── engine.py             # GBM Monte Carlo path generator
│   ├── options.py            # European, Asian, and Barrier classes
│   └── pricer.py             # Valuation and Greeks calculation
│
├── notebooks/
│   └── showcase.ipynb        # Visualizations and usage examples
│
├── tests/
│   └── test_pricing.py       # Black-Scholes validation tests
│
├── requirements.txt
└── README.md