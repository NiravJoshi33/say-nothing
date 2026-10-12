import torch
import torch.nn as nn

# setting manual seed to ensure our data stays same across re-runs
torch.manual_seed(10)

TRAINING_DATASET_SHAPE = (20, 1) #(number of entries in tensor, number of items within each entry)
random_xs = torch.rand(TRAINING_DATASET_SHAPE)

random_ys = 2 * random_xs + 1

layer = nn.Linear(in_features=1, out_features=1) # model that will guess the answer



learning_rate = 1e-1
epochs = 1000
optimizer = torch.optim.SGD(layer.parameters(), lr=learning_rate)
criterion = nn.MSELoss()

for i in range(epochs):

    predictions = layer(random_xs)

   
    loss = criterion(predictions, random_ys)

    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    print(loss.item())

print("weight: ", layer.weight)
print("bias: ", layer.bias)