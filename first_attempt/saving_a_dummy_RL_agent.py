import gym
import pickle
import json

# Define a simple RL agent class
class SimpleAgent:
    def __init__(self, num_actions):
        self.num_actions = num_actions

    def predict(self, observation):
        # Randomly choose an action
        import random
        return random.randint(0, self.num_actions - 1)

# Create a gym environment
env = gym.make("CartPole-v1")

# Save the action space (number of possible actions)
action_space = env.action_space.n  # Extract number of actions (e.g., 2 for CartPole)
with open("action_space.json", "w") as f:
    json.dump({"num_actions": action_space}, f)
print("✅ Action space saved to 'action_space.json'")

# Initialize the agent with the number of actions
agent = SimpleAgent(num_actions=action_space)

# Save the agent to a file
with open("rl_agent.pkl", "wb") as f:
    pickle.dump(agent, f)
print("✅ RL agent saved as 'rl_agent.pkl'")