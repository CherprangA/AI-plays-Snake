Updates:
```
We got the RL agent working in the web, this is huge

but the RL agent is so bad, It's MlpPolicy which can't use CUDA when training and
performs very BAD
```

Next update:
```
Use CnnPolicy
which means, we can train using CUDA, so training is faster

but we can still test it using CPU, which means it works with pygbag / web
```