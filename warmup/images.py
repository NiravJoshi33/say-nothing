from PIL import Image
from transformers import AutoProcessor, AutoModel
import torch

with Image.open("data/raw/chart_bar.jpg") as img:
    converted = img.convert("RGB")
    print(converted.size)
    print(converted.mode)

    processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")
    result = processor(images = converted, return_tensors="pt")
   

    model = AutoModel.from_pretrained("google/siglip-base-patch16-224")

    with torch.no_grad():
        outputs = model.get_image_features(**result)

        # print(outputs)
        print(outputs["last_hidden_state"])
        print(outputs["pooler_output"])
        print(outputs["last_hidden_state"].shape)
        print(outputs["pooler_output"].shape)