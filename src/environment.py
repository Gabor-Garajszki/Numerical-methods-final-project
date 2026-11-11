class MarketEnvironment:
    """contains the characteristic of that stock"""

    def __init__(self, S0: float, r: float, sigma: float):
        self.S0 = S0
        self.r = r
        self.sigma = sigma

    def __repr__(self):
        return f"MarketEnvironment(S0={self.S0}, r={self.r}, sigma={self.sigma})"