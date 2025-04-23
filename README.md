<div align="center">

###### ------>ACTIVITY PAUSED<------
I have realized that my understanding of neural networks and reinforcement learning is not sufficient for this project at the moment. I plan to resume once I have gained more knowledge in these areas.  

In the meantime, you can still view the demo, which currently uses the A* + Flood-fill approach.  

</div>

# AI-plays-Snake

[Watch the demo](https://cherpranga.github.io/AI-plays-Snake/)

## Description

Training a Reinforcement Learning (RL) agent to play the classic snake game.

The snake game is developed from scratch using PyGame. Since browsers don't natively support PyGame games, Pygbag is used to convert the game to WebAssembly and deploy it on GitHub Pages.

### **Main Challenges**

- Unlike JavaScript, games made with PyGame don't run natively in browsers. Pygbag is required to convert PyGame to WebAssembly to make it browser-compatible and hostable on GitHub Pages.
- Pygbag doesn't support Gym, Gymnasium, and several other libraries. While training can be done using Gym and CUDA, testing cannot use these libraries if the game is to run in a browser via Pygbag.
- Developing the game (test) code without using Gym or related libraries is highly challenging.

### **What's Been Done So Far**

- Base game mechanics have been implemented.
- Training and testing have been conducted without using neural networks, resulting in poor RL agent performance.

### **What Needs to Be Done**

- Train and test using `CnnPolicy` (leveraging neural networks).

### **Expected Outcome**

- While the snake game appears simple, training an RL agent for it reveals its complexity.
- The agent must track food, walls, the snake's body, and other hidden factors.
- The agent must make optimal decisions to ensure its path leads to food while avoiding self-collision or confinement.
- Eventually, the project may reach a point where the RL agent's performance cannot be further improved.
- If a successful RL agent cannot be achieved, the project may pivot to an algorithmic approach.
<div align="center">

### **ggez**

</div>
