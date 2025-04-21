import torch

# Check if GPU is available
if torch.cuda.is_available():
    print("GPU is available for training.")
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
else:
    print("GPU is not available. Training will use the CPU.")