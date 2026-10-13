from PIL import Image
from transformers import AutoProcessor, AutoModel
import torch
from data_loader import load_csv
import numpy as np
from pathlib import Path




def get_embeddings():
    model = AutoModel.from_pretrained("google/siglip-base-patch16-224")
    processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")
    
    data = load_csv()

    images = []

    for row in data:
        file_name = row["filename"]
        with Image.open(f"data/raw/{file_name}") as img:
            images.append(img.convert("RGB"))

    
    result = processor(images = images, return_tensors="pt")

    with torch.no_grad():
        outputs = model.get_image_features(**result)

        # print(outputs)
        # print(outputs["last_hidden_state"])
        # print(outputs["pooler_output"])
        # print(outputs["last_hidden_state"].shape)
        # print(outputs["pooler_output"].shape)

        return outputs["pooler_output"]



# embeddings = get_embeddings()

def save_embeddings(embeddings, path):
    np.save(path, embeddings)

def load_embeddings(path):
    
    data = np.load(path)
    return data


def get_or_create_embeddings(file_path):
    try:
        path = Path(file_path)
        embeddings = load_embeddings(path)
        print("loaded from cache")
    except FileNotFoundError:
        embeddings = get_embeddings()
        print("generated new embeddings")
        save_embeddings(embeddings, file_path)

    return embeddings

embd = get_or_create_embeddings("data/embeddings.npy")



        