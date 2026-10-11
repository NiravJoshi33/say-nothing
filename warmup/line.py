import torch

# setting manual seed to ensure our data stays same across re-runs
torch.manual_seed(10)

TRAINING_DATASET_SHAPE = (20, 1) #(number of entries in tensor, number of items within each entry)
random_xs = torch.rand(TRAINING_DATASET_SHAPE)


random_ys = random_xs.mul(2).add(1)

print("x: ", random_xs)
print("y: ", random_ys)
