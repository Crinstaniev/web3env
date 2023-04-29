from web3env.core.envs.rl_env import CustomEnv

def load_env(validator_size=100, initial_honest_proportion=0.5, limit=256):
    env = CustomEnv(
        validator_size=validator_size,
        initial_honest_proportion=initial_honest_proportion,
        limit=limit
    )
    return env

def load_sample_validator(env: CustomEnv):
    validator = env.validators[0]
    return validator