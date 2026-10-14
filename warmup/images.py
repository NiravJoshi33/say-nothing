from PIL import Image
from transformers import AutoProcessor, AutoModel
import torch
from data_loader import load_csv
import numpy as np
from pathlib import Path
import torch.nn as nn




def get_embeddings(data, image_dir= "data/raw/"):
    model = AutoModel.from_pretrained("google/siglip-base-patch16-224")
    processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")
    

    images = []

    for row in data:
        file_name = row["filename"]
        with Image.open(f"{image_dir}{file_name}") as img:
            images.append(img.convert("RGB"))

    
    result = processor(images = images, return_tensors="pt")

    with torch.no_grad():
        outputs = model.get_image_features(**result)

        return outputs["pooler_output"]



# embeddings = get_embeddings()

def save_embeddings(embeddings, path):
    np.save(path, embeddings)

def load_embeddings(path):
    
    data = np.load(path)
    return data


def get_or_create_embeddings(file_path, data, image_dir):
    try:
        path = Path(file_path)
        embeddings = torch.from_numpy(load_embeddings(path))
        print("loaded from cache")
    except FileNotFoundError:
        embeddings = get_embeddings(data, image_dir)
        print("generated new embeddings")
        save_embeddings(embeddings, file_path)

    return embeddings


actions_map = {
    "refuse": 0,
    "empty": 1,
    "caption": 2
}
number_to_action_map = {v: k for k, v in actions_map.items()}

torch.manual_seed(10)
layer = nn.Linear(in_features=768, out_features=3)

learning_rate = 1e-1
epochs = 1000
optimizer = torch.optim.SGD(layer.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss()

data = load_csv(path="data/labels.csv")
new_data = load_csv(path="data/test/labels.csv")

validation_row_positions =  [3, 9, 5, 15]
training_data_pos = [i for i in range(len(data)) if i not in validation_row_positions]

embeddings = get_or_create_embeddings("data/embeddings.npy", data, "data/raw/")
new_embeddings = get_or_create_embeddings("data/new_embeddings.npy", new_data, "data/test/raw/")
new_data_actions = [actions_map[new_data[i]["action"]] for i in range(len(new_data))]
training_embeddings = embeddings[training_data_pos]
validation_embeddings = embeddings[validation_row_positions]
print(training_embeddings.shape)
print(validation_embeddings.shape)
# print(embeddings)



correct_actions_arr = [actions_map[data[i]["action"]] for i in training_data_pos]
correct_actions = torch.tensor(correct_actions_arr)

eval_correct_actions_arr = [actions_map[data[i]["action"]] for i in validation_row_positions]
eval_actions = torch.tensor(eval_correct_actions_arr)

for i in range(epochs):

    predictions = layer(training_embeddings)

   
    loss = criterion(predictions, correct_actions)

    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

with torch.no_grad():
    val_predictions = layer(validation_embeddings)

    val_predictions_indices = torch.argmax(val_predictions, dim=1)

    accurate_predicts = 0
    for i, row in enumerate(val_predictions_indices):
        
        if number_to_action_map[row.item()] == number_to_action_map[eval_actions[i].item()]:
            accurate_predicts += 1

    print("validation accuracy: ", accurate_predicts * 100 / len(val_predictions_indices))

with torch.no_grad():
    training_predictions = layer(training_embeddings)

    train_predictions_indices = torch.argmax(training_predictions, dim=1)

    accurate_predicts = 0
    for i, row in enumerate(train_predictions_indices):
        
        if number_to_action_map[row.item()] == number_to_action_map[correct_actions[i].item()]:
            accurate_predicts += 1

    print("training accuracy: ", accurate_predicts * 100 / len(train_predictions_indices))



with torch.no_grad():
    new_predictions = layer(new_embeddings)
    
    new_predictions_indices = torch.argmax(new_predictions, dim=1)

    accurate_predicts = 0
    for i, row in enumerate(new_predictions_indices):
        
        if number_to_action_map[row.item()] == number_to_action_map[new_data_actions[i]]:
            accurate_predicts += 1

    print(f"{accurate_predicts} accurate predictions out of total {len(new_predictions_indices)} images")


