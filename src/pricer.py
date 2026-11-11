import numpy as np
from src.environment import MarketEnvironment
from src.engine import MonteCarloEngine
from src.options import Option

class Pricer:
     
    def __init__(self, engine: MonteCarloEngine):
        self.engine = engine

    def calculate_price(self, env: MarketEnvironment, option: Option) -> float:
        """Using the other src objects it calculates the fair value"""

        paths = self.engine.simulate_gbm(env, option.T)
        payoffs = option.get_payoff(paths)
        expected_payoff = np.mean(payoffs)
        discount_factor = np.exp(-env.r * option.T)
        
        return expected_payoff * discount_factor

    def calculate_greeks(self, env: MarketEnvironment, option: Option) -> dict:
        """it returns the greeks and the fair value: fair value, delta, vega, rho, gamma, theta"""
        V_base = self.calculate_price(env, option)

        #delta and gamma: it calculates the derivative of the fair value if the spot value changes 1% (and its derivative)
        dS = env.S0 * 0.01
        env_S_up = MarketEnvironment(env.S0 + dS, env.r, env.sigma)
        env_S_down = MarketEnvironment(env.S0 - dS, env.r, env.sigma)
        
        V_S_up = self.calculate_price(env_S_up, option)
        V_S_down = self.calculate_price(env_S_down, option)
        
        delta = (V_S_up - V_S_down) / (2 * dS)
        gamma = (V_S_up - 2 * V_base + V_S_down) / (dS ** 2)

        #similar to the previous one, but this time the sigma changes 1%
        dSigma = 0.01
        env_sig_up = MarketEnvironment(env.S0, env.r, env.sigma + dSigma)
        env_sig_down = MarketEnvironment(env.S0, env.r, max(0.001, env.sigma - dSigma))
        
        vega = (self.calculate_price(env_sig_up, option) - self.calculate_price(env_sig_down, option)) / (2 * dSigma)

        #in this case the risk free factor
        dR = 0.01
        env_r_up = MarketEnvironment(env.S0, env.r + dR, env.sigma)
        env_r_down = MarketEnvironment(env.S0, env.r - dR, env.sigma)
        
        rho = (self.calculate_price(env_r_up, option) - self.calculate_price(env_r_down, option)) / (2 * dR)

        #the theta gives the sensitiveness if 1 day passes without anything else changes
        dT = 1.0 / 252.0
        if option.T - dT > 0:
            original_T = option.T
            option.T = option.T - dT
            
            V_T_down = self.calculate_price(env, option)        #the one day later fair value
            
            option.T = original_T
            
            theta = (V_T_down - V_base) / dT 
        else:
            theta = 0.0

        return {
            "Price": V_base,
            "Delta": delta,
            "Gamma": gamma,
            "Vega": vega,
            "Rho": rho,
            "Theta": theta
        }