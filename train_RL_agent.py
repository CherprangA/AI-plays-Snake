import json
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env
from snake_env import SnakeEnv

# Initialize the Snake environment
env = SnakeEnv()

# Check if the environment is valid
check_env(env)

# Wrap the environment for vectorized training
vec_env = make_vec_env(lambda: env, n_envs=1)

# Train the RL agent using PPO with CnnPolicy
model = PPO("CnnPolicy", vec_env, verbose=1, device="auto", policy_kwargs={"normalize_images": False})
print("🚀 Training the RL agent...")
model.learn(total_timesteps=10000, progress_bar=True)
print("✅ Training completed!")

# Save the policy weights
model.save("snake_cnn_policy")
print("✅ Policy saved to snake_cnn_policy.zip")

# Save the action space
action_space = {
    "actions": ["up", "down", "left", "right"],
    "num_actions": 4
}
with open("snake_action_space.json", "w") as f:
    json.dump(action_space, f)
print("✅ Action space saved to snake_action_space.json")