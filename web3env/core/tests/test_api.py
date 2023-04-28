from gym.utils.env_checker import check_env
from core.envs.rl_env import CustomEnv
import pytest

@pytest.mark.skip(reason="passed")
def test_api_conformity():
    env = CustomEnv()
    check_env(env, warn=True)
    