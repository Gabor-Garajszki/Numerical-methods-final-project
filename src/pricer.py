import numpy as np
from src.environment import MarketEnvironment
from src.engine import MonteCarloEngine
from src.options import Option

class Pricer:
     
    def __init__(self, engine: MonteCarloEngine):
        self.engine = engine

    def calculate_price(self, env: MarketEnvironment, option: Option) -> float:
        
        paths = self.engine.simulate_gbm(env)
        payoffs = option.get_payoff(paths)
        expected_payoff = np.mean(payoffs)
        discount_factor = np.exp(-env.r * env.T)
        
        return expected_payoff * discount_factor

    def calculate_greeks(self, env: MarketEnvironment, option: Option) -> dict:
        
        V_base = self.calculate_price(env, option)

        dS = env.S0 * 0.01
        env_S_up = MarketEnvironment(env.S0 + dS, env.r, env.sigma, env.T)
        env_S_down = MarketEnvironment(env.S0 - dS, env.r, env.sigma, env.T)
        
        V_S_up = self.calculate_price(env_S_up, option)
        V_S_down = self.calculate_price(env_S_down, option)
        
        delta = (V_S_up - V_S_down) / (2 * dS)
        gamma = (V_S_up - 2 * V_base + V_S_down) / (dS ** 2)

        dSigma = 0.01
        env_sig_up = MarketEnvironment(env.S0, env.r, env.sigma + dSigma, env.T)
        env_sig_down = MarketEnvironment(env.S0, env.r, max(0.001, env.sigma - dSigma), env.T)
        
        vega = (self.calculate_price(env_sig_up, option) - self.calculate_price(env_sig_down, option)) / (2 * dSigma)

        dR = 0.01
        env_r_up = MarketEnvironment(env.S0, env.r + dR, env.sigma, env.T)
        env_r_down = MarketEnvironment(env.S0, env.r - dR, env.sigma, env.T)
        
        rho = (self.calculate_price(env_r_up, option) - self.calculate_price(env_r_down, option)) / (2 * dR)

        dT = 1.0 / 252.0
        if env.T - dT > 0:
            env_T_down = MarketEnvironment(env.S0, env.r, env.sigma, env.T - dT)
            V_T_down = self.calculate_price(env_T_down, option)
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