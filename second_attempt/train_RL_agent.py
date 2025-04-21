import json
import numpy as np
from stable_baselines3 import PPO
from snake_env import SnakeEnv
from tqdm import tqdm
import torch

# Initialize the Snake environment
env = SnakeEnv()
# Verify the observation space
print(f"Observation space: {env.observation_space.shape}")  # Should print (5,)

# Train the RL agent using PPO
model = PPO("MlpPolicy", env, verbose=1, device="cuda" if torch.cuda.is_available() else "cpu")
print("🚀 Training the RL agent...")
model.learn(total_timesteps=10000, progress_bar=True)
print("✅ Training completed!")

# Save the policy weights
policy_weights = {k: v.tolist() for k, v in model.policy.state_dict().items()}
print(f"Shape of first layer weights: {np.array(policy_weights['mlp_extractor.policy_net.0.weight']).shape}")  # Debug
with open("snake_policy_weights.json", "w") as f:
    json.dump(policy_weights, f)
print("✅ Policy weights saved to snake_policy_weights.json")

# Save the action space
action_space = {
    "actions": ["up", "down", "left", "right"],
    "num_actions": 4
}
with open("snake_action_space.json", "w") as f:
    json.dump(action_space, f)
print("✅ Action space saved to snake_action_space.json")