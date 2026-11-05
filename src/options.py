import numpy as np
from abc import ABC, abstractmethod

class Option(ABC):
    
    def __init__(self, strike: float, option_type: str = 'call'):
        self.strike = strike
        self.option_type = option_type.lower()
        
    @abstractmethod
    def get_payoff(self, price_paths: np.ndarray) -> np.ndarray:
        
        pass

class EuropeanOption(Option):
    
    def get_payoff(self, price_paths: np.ndarray) -> np.ndarray:
        
        S_T = price_paths[-1, :] 
        
        if self.option_type == 'call':
            return np.maximum(S_T - self.strike, 0)
        elif self.option_type == 'put':
            return np.maximum(self.strike - S_T, 0)
        else:
            raise ValueError("Az option_type csak 'call' vagy 'put' lehet.")

class AsianOption(Option):
    
    def get_payoff(self, price_paths: np.ndarray) -> np.ndarray:
        
        S_mean = np.mean(price_paths, axis=0)
        
        if self.option_type == 'call':
            return np.maximum(S_mean - self.strike, 0)
        elif self.option_type == 'put':
            return np.maximum(self.strike - S_mean, 0)
        else:
            raise ValueError("Az option_type csak 'call' vagy 'put' lehet.")


class BarrierOption(Option):

    def __init__(self, strike: float, barrier_level: float, option_type: str = 'call'):
        
        super().__init__(strike, option_type)
        self.barrier_level = barrier_level

    def get_payoff(self, price_paths: np.ndarray) -> np.ndarray:
        
        S_T = price_paths[-1, :]
        
        if self.option_type == 'call':
            payoff = np.maximum(S_T - self.strike, 0)
        elif self.option_type == 'put':
            payoff = np.maximum(self.strike - S_T, 0)
        else:
            raise ValueError("Az option_type csak 'call' vagy 'put' lehet.")
        
        min_prices = np.min(price_paths, axis=0)
        
        knocked_out = min_prices <= self.barrier_level
        
        payoff[knocked_out] = 0.0
        
        return payoff