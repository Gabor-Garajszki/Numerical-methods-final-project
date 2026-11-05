import numpy as np
from src.environment import MarketEnvironment

class MonteCarloEngine:
    def __init__(self, num_paths: int, num_steps: int):
        self.num_paths = num_paths
        self.num_steps = num_steps

    def simulate_gbm(self, env: MarketEnvironment) -> np.ndarray:
        dt = env.T / self.num_steps
        
        Z = np.random.standard_normal((self.num_steps, self.num_paths))
        
        dW = Z * np.sqrt(dt)
        W = np.cumsum(dW, axis=0)
        
        time_steps = np.linspace(dt, env.T, self.num_steps)[:, np.newaxis]
        
        drift = (env.r - 0.5 * env.sigma**2) * time_steps
        diffusion = env.sigma * W
        
        S = env.S0 * np.exp(drift + diffusion)
        
        S_0_row = np.full((1, self.num_paths), env.S0)
        paths = np.vstack((S_0_row, S))
        
        return paths