import os
from scripts.scrapper import scrape_and_store_images
from app.predictor import batch_classify_images
from visualize.plot import plot_top_3_brands



def run_pipeline():
    # 1. Scrape images
    site_url = "https://www.flickr.com/groups/carexpressions/pool/" # <-- Change to your site
    save_dir = "static/raw_images" 
    img_count = 30  # Scrape 30 images for example
    scrape_and_store_images(site_url, save_dir, limit=img_count)
    # 2. Batch prediction
    image_paths = [os.path.join(save_dir, f) for f in os.listdir(save_dir)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    brand_counts = batch_classify_images(image_paths)
    # 3. Draw bar chart
    plot_top_3_brands(brand_counts)
