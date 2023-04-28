import gym
from core.envs.rl_env import CustomEnv
import pytest
import pandas as pd


# @pytest.mark.skip(reason="passed")
def test_env():
    env = CustomEnv()
    observation, info = env.reset()

    info_records = []

    for _ in range(1000):
        # agent policy that uses the observation and info
        action = env.action_space.sample()
        observation, reward, terminated, info = env.step(action)

        info_records.append(info)

        if terminated:
            break

    df = pd.DataFrame(info_records)

    env.close()
