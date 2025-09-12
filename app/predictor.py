import torch
from PIL import Image
from torchvision import transforms, models
import torch.nn as nn
import os

MODEL_PATH = os.path.join('model', 'car_brand_classifier.pt')
CLASSES = ["audi", "bmw", "lamborgini", "mercedes", "others", "porshe", "toyota"]

def load_trained_model():
    model = models.mobilenet_v2(pretrained=False)
    model.classifier[1] = nn.Linear(model.last_channel, len(CLASSES))
    model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
    model.eval()
    return model

def batch_classify_images(image_paths):
    model = load_trained_model()
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    brand_counts = {}
    for img_path in image_paths:
        img = Image.open(img_path).convert('RGB')
        img_tensor = transform(img).unsqueeze(0)
        with torch.no_grad():
            output = model(img_tensor)
            pred = output.argmax(1).item()
        brand = CLASSES[pred]
        brand_counts[brand] = brand_counts.get(brand, 0) + 1
    return brand_counts
