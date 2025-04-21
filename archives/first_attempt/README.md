This is the first attempt trying to train the AI model to Play the snake game using the Q-Learning

The mode is trained on CPU and simple observatsion space like
```
Snake Head position
Food position
Length of the snake
```

Pros:
```
Simple observation space 
```

Cons:
```
Again, just a simple observation space so, 
the snake dies getting like 5 points becuase it bites its own body
collides with wall
the current version of code doesn't work with `pygabg` so, can't run on broswer
```

Updates I want to make:
```
Update the code to run using CUDA
Update the observation space to include the snake body locations
Update the rewards system
update the code to work with pygbag
```

THE END

