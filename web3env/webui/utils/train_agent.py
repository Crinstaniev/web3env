import json
import os

import numpy as np
import pandas as pd
from stable_baselines3 import A2C

from web3env.core.envs.rl_env import CustomEnv

EPOCHS = 30
LIMIT = 256
TAKES = 8
SEED = 42

def train_model(env: CustomEnv, log_interval: int = 100):
    DATA_PATH = os.environ.get('DATA_PATH')
    # clean data folder
    if os.path.exists(DATA_PATH + '/a2c.json'):
        os.remove(DATA_PATH + '/a2c.json')
    if os.path.exists(DATA_PATH + '/a2c.zip'):
        os.remove(DATA_PATH + '/a2c.zip')
    if os.path.exists(DATA_PATH + '/a2c.csv'):
        os.remove(DATA_PATH + '/a2c.csv')
    
    log = []
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
                print('writing to trainning log')
                json.dump(log, f)
    
    np.random.seed(SEED)
    env = CustomEnv()
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

    df = pd.DataFrame(info_records)
    df.to_csv(os.path.join(DATA_PATH, 'a2c.csv'), index=False)