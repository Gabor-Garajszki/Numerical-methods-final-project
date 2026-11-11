import numpy as np
from abc import ABC, abstractmethod

class Option(ABC):
    """Abstract base class: contains the strike price, the maturity time and the put or call option type"""
    def __init__(self, strike: float, T: float, option_type: str = 'call'):
        self.strike = strike
        self.T = T
        self.option_type = option_type.lower()
        
    @abstractmethod
    def get_payoff(self, price_paths: np.ndarray) -> np.ndarray:
        
        pass

class EuropeanOption(Option):
    
    def get_payoff(self, price_paths: np.ndarray) -> np.ndarray:
        
        S_T = price_paths[-1, :]        #only the last day is what matters
        
        if self.option_type == 'call':
            return np.maximum(S_T - self.strike, 0)
        elif self.option_type == 'put':
            return np.maximum(self.strike - S_T, 0)
        else:
            raise ValueError("the option type only 'call' or 'put' can be")

class AsianOption(Option):
    
    def get_payoff(self, price_paths: np.ndarray) -> np.ndarray:
        
        S_mean = np.mean(price_paths, axis=0)       #the mean value for each path
        
        if self.option_type == 'call':
            return np.maximum(S_mean - self.strike, 0)
        elif self.option_type == 'put':
            return np.maximum(self.strike - S_mean, 0)
        else:
            raise ValueError("the option type only 'call' or 'put' can be")


class BarrierOption(Option):

    def __init__(self, strike: float, T: float, barrier_level: float, option_type: str = 'call'):     #the init contains the barrier level additionally
        
        super().__init__(strike, T, option_type)
        self.barrier_level = barrier_level

    def get_payoff(self, price_paths: np.ndarray) -> np.ndarray:
        
        S_T = price_paths[-1, :]
        
        if self.option_type == 'call':
            payoff = np.maximum(S_T - self.strike, 0)
        elif self.option_type == 'put':
            payoff = np.maximum(self.strike - S_T, 0)
        else:
            raise ValueError("the option type only 'call' or 'put' can be")
        
        min_prices = np.min(price_paths, axis=0)        #the lowest value of each path
        
        knocked_out = min_prices <= self.barrier_level      #boolean mask
        
        payoff[knocked_out] = 0.0
        
        return payoff