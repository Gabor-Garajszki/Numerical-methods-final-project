import numpy as np
from src.environment import MarketEnvironment

class MonteCarloEngine:
    """Stohastic monte carlo engine. Can init it with different accuracy, and calculate the stock's price in n paths for T year"""

    def __init__(self, num_paths: int, days_per_year: int = 252):
        """num_paths: more path for more accuracy: ~ 1/sqrt(n)
        days_per_year: normally this is 252, but just in case I made it changeable"""

        self.num_paths = num_paths
        self.days_per_year = days_per_year

    def simulate_gbm(self, env: MarketEnvironment, T: float) -> np.ndarray:
        """calculate the stock's price in n paths for T year"""

        num_steps = int(T * self.days_per_year)         #calculates how many steps will be till maturity
        
        dt = 1.0 / self.days_per_year       # one step equals one day
        
        Z = np.random.standard_normal((num_steps, self.num_paths))      #makes a matrix with random numbers (the variance for each day) for each day in every path
        
        dw = Z * np.sqrt(dt)        #from the normal distribution random nuber it gives the daily %of the stohastic change
        W = np.cumsum(dw, axis=0)       #for the matrix operation we need the cumulative summa
        
        time_steps = np.linspace(dt, T, num_steps)[:, np.newaxis]       #timeline rill the maturity
        
        drift = (env.r - 0.5 * env.sigma**2) * time_steps       #the deterministic part
        diffusion = env.sigma * W       #the stoc's own volatility
        
        S = env.S0 * np.exp(drift + diffusion) 
        
        S_0_row = np.full((1, self.num_paths), env.S0)      #the t0 with s0 prices 1 x paths matrix
        paths = np.vstack((S_0_row, S))     #adds the t0 prices into the matrix
        
        return paths