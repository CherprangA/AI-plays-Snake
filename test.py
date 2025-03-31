import gym
import numpy as np

env = gym.make("MountainCar-v0", render_mode="human")
env.reset()

print(env.observation_space.high)
print(env.observation_space.low)
print(env.action_space.n)

DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
DISCRETE_OS_WINDOW_SIZE = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

print(DISCRETE_OS_WINDOW_SIZE)

q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))

print(q_table.shape)
print(q_table)

# done = False

# while not done:
#     action = 2
#     new_state, reward, done, truncated, info = env.step(action)
#     env.render()
#     print("action: {}, reward: {}".format(action, reward))

# env.close()