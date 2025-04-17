# Define the SimpleAgent class (same as in train_and_save.py)
class SimpleAgent:
    def __init__(self, num_actions):
        self.num_actions = num_actions

    def predict(self, observation):
        import random
        return random.randint(0, self.num_actions - 1)