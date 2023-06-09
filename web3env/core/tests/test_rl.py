import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from core.envs.rl_env import CustomEnv
from stable_baselines3 import A2C, DDPG, PPO
from stable_baselines3.common import results_plotter
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.results_plotter import plot_results
from tqdm import tqdm

EPOCHS = 30
LIMIT = 256
TAKES = 8
SEED = 42

initial_proportions = [0.001, 0.1, 0.2, 0.3,
                       0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.999]

# @pytest.mark.skip()
def test_a2c():
    log = []
    log_interval = 1000
    DATA_PATH = os.environ.get('DATA_PATH')
    def callback_fn(locals_, globals_):
        rewards = locals_['rewards']
        infos = locals_['infos']
        num_timesteps = locals_['self'].num_timesteps
        
        if num_timesteps % log_interval == 0:
            honest_proportion = infos[0]['honest_proportion']
            round = infos[0]['round']
            total_honest_effective_balance = infos[0]['total_honest_effective_balance']
            alpha = infos[0]['alpha']
            sum_balance_honest = infos[0]['sum_balance_honest']
            sum_balance_all = infos[0]['sum_balance_all']
            reward = rewards[0]
            
            payload = dict(
                honest_proportion=float(honest_proportion),
                round=int(round),
                total_honest_effective_balance=int(total_honest_effective_balance),
                alpha=float(alpha),
                sum_balance_honest=int(sum_balance_honest) or 0,
                sum_balance_all=int(sum_balance_all) or 0,
                reward=float(reward),
            )
            
            # append to json
            log.append(payload)
            with open(DATA_PATH + '/a2c.json', 'w') as f:
                json.dump(log, f)
            
    
    np.random.seed(SEED)
    env = CustomEnv()

    observation = env.reset()

    timesteps = LIMIT * 32

    model = A2C("MultiInputPolicy", env, verbose=0)

    model.learn(total_timesteps=timesteps, callback=callback_fn)

    model.save(DATA_PATH + '/a2c')

    # test model
    observation = env.reset()

    info_records = []
    while 1:
        action, _states = model.predict(observation, deterministic=True)
        observation, reward, done, info = env.step(action)
        info_records.append(info)
        if done:
            break
        
    
