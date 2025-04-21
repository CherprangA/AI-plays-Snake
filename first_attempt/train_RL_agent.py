import json
import torch
from stable_baselines3 import PPO
from snake_env import SnakeEnv
from tqdm import tqdm

# Initialize the Snake environment
env = SnakeEnv()

# Define the action space (0: up, 1: down, 2: left, 3: right)
action_space = {
    "actions": ["up", "down", "left", "right"],
    "num_actions": 4
}

# Save the action space to a JSON file
with open("snake_action_space.json", "w") as f:
    json.dump(action_space, f)
print("✅ Action space saved to snake_action_space.json")

# Train the RL agent using PPO
model = PPO("MlpPolicy", env, verbose=1, device="cpu")  # Force CPU usage
print("🚀 Training the RL agent...")
# Define total timesteps
total_timesteps = int(1e10)
total_timesteps = 100000

# Create a progress bar
with tqdm(total=total_timesteps, desc="Training Progress", unit="step") as pbar:
    def callback(_locals, _globals):
        pbar.n = _locals["self"].num_timesteps
        pbar.update(0)
        return True

    # Train the model with the callback
    model.learn(total_timesteps=total_timesteps, callback=callback)
print("✅ Training completed!")

# Save the trained model using stable-baselines3's save method
model.save("snake_rl_agent")
print("✅ Trained RL agent saved to snake_rl_agent.zip")

# Extract and save the policy weights
policy = model.policy
torch.save(policy, "snake_policy_full.pth")
print("✅ Policy weights saved to snake_policy_full.pth")

# Test the trained model
# print("🎮 Testing the trained agent...")
# obs = env.reset()
# done = False
# while not done:
#     action, _ = model.predict(obs)
#     obs, reward, done, info = env.step(action)
#     env.render()