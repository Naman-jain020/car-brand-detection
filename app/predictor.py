"""
Car brand prediction module
Loads the trained model and predicts brands from images
"""

import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import os
from collections import Counter

# Car brand labels - MUST match your training classes
BRAND_LABELS = ["audi", "bmw", "lamborgini", "mercedes", "others", "porshe", "toyota"]

class CarBrandPredictor:
    def __init__(self, model_path='model/car_brand_classifier.pt'):
        """Initialize the predictor with the trained model"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Build model architecture (MobileNetV2)
        self.model = models.mobilenet_v2(pretrained=False)
        self.model.classifier[1] = nn.Linear(self.model.last_channel, len(BRAND_LABELS))
        
        # Load trained weights
        try:
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            print(f"✓ Model loaded from {model_path}")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            raise
        
        # Define image transformations (same as training)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def predict_single(self, image_path):
        """
        Predict brand for a single image
        
        Args:
            image_path: Path to the image file
        
        Returns:
            Predicted brand name
        """
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(image_tensor)
                _, predicted = torch.max(outputs, 1)
                brand_idx = predicted.item()
            
            # Return brand name
            if brand_idx < len(BRAND_LABELS):
                return BRAND_LABELS[brand_idx]
            else:
                return 'Unknown'
                
        except Exception as e:
            print(f"Error predicting {image_path}: {e}")
            return None
    
    def predict_batch(self, image_dir):
        """
        Predict brands for all images in a directory
        
        Args:
            image_dir: Directory containing images
        
        Returns:
            Dictionary with brand counts
        """
        predictions = []
        
        # Get all image files
        image_files = [f for f in os.listdir(image_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            print("No images found in directory!")
            return {}
        
        print(f"\nPredicting brands for {len(image_files)} images...")
        
        for idx, filename in enumerate(image_files):
            image_path = os.path.join(image_dir, filename)
            brand = self.predict_single(image_path)
            
            if brand:
                predictions.append(brand)
                print(f"[{idx+1}/{len(image_files)}] {filename}: {brand}")
        
        # Count occurrences
        brand_counts = dict(Counter(predictions))
        
        print(f"\n{'='*50}")
        print("Prediction Summary:")
        for brand, count in sorted(brand_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {brand}: {count}")
        print(f"{'='*50}\n")
        
        return brand_counts


def predict_brands(image_dir):
    """
    Main function to predict brands from a directory of images
    
    Args:
        image_dir: Directory containing car images
    
    Returns:
        Dictionary mapping brand names to counts
    """
    try:
        predictor = CarBrandPredictor()
        return predictor.predict_batch(image_dir)
    except Exception as e:
        print(f"Error in prediction: {e}")
        raise


# Alternative: Direct batch classification (like your original code)
def batch_classify_images(image_paths):
    """
    Classify a list of image paths (legacy function)
    
    Args:
        image_paths: List of image file paths
    
    Returns:
        Dictionary mapping brand names to counts
    """
    # Load model
    model = models.mobilenet_v2(pretrained=False)
    model.classifier[1] = nn.Linear(model.last_channel, len(BRAND_LABELS))
    model.load_state_dict(torch.load('model/car_brand_classifier.pt', map_location='cpu'))
    model.eval()
    
    # Transform
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    brand_counts = {}
    
    for img_path in image_paths:
        try:
            img = Image.open(img_path).convert('RGB')
            img_tensor = transform(img).unsqueeze(0)
            
            with torch.no_grad():
                output = model(img_tensor)
                pred = output.argmax(1).item()
            
            brand = BRAND_LABELS[pred]
            brand_counts[brand] = brand_counts.get(brand, 0) + 1
            
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            continue
    
    return brand_counts


if __name__ == "__main__":
    # Test the predictor
    test_dir = "../static/raw_images"
    if os.path.exists(test_dir):
        results = predict_brands(test_dir)
        print(f"\nFinal results: {results}")
    else:
        print(f"Test directory not found: {test_dir}")
