"""
Gradio App for Car Brand Detection System
"""

import gradio as gr
import os
import torch
from scripts.scrapper import scrape_flickr_simple
from app.predictor import predict_brands
from visualize.plot import create_brand_chart
from PIL import Image

# Create necessary directories
os.makedirs('static/raw_images', exist_ok=True)

def scrape_and_analyze(num_images):
    """
    Scrape images and analyze brands
    """
    try:
        # Validate input
        if num_images < 10 or num_images > 50:
            return "❌ Please enter a number between 10 and 50", None
        
        # Step 1: Scrape images
        status = f"🔄 Scraping {num_images} images..."
        yield status, None
        
        images_scraped = scrape_flickr_simple(
            url="https://www.flickr.com/groups/carexpressions/pool/",
            save_dir="static/raw_images",
            limit=num_images
        )
        
        if images_scraped == 0:
            return "❌ No images could be scraped. Please try again.", None
        
        # Step 2: Predict brands
        status = f"✓ Scraped {images_scraped} images\n🔄 Analyzing brands..."
        yield status, None
        
        brand_counts = predict_brands('static/raw_images')
        
        if not brand_counts:
            return "❌ Could not detect any brands.", None
        
        # Step 3: Create chart
        chart_path = "static/brand_chart.png"
        create_brand_chart(brand_counts, chart_path)
        
        # Prepare results text
        results = f"✅ Analysis Complete!\n\n📊 Brand Distribution:\n"
        for brand, count in sorted(brand_counts.items(), key=lambda x: x[1], reverse=True):
            results += f"  • {brand.capitalize()}: {count}\n"
        
        return results, chart_path
        
    except Exception as e:
        return f"❌ Error: {str(e)}", None

# Create Gradio Interface
with gr.Blocks(theme=gr.themes.Soft(), title="🚗 Car Brand Detection") as demo:
    
    gr.Markdown("""
    # 🚗 Car Brand Detection System
    
    An AI-powered system that scrapes car images and detects brands using deep learning.
    
    ### How to use:
    1. Choose number of images to scrape (10-50)
    2. Click "Start Analysis"
    3. Wait for results
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            num_images = gr.Slider(
                minimum=10,
                maximum=50,
                value=20,
                step=1,
                label="Number of Images to Scrape",
                info="More images = better accuracy but slower"
            )
            
            submit_btn = gr.Button("🚀 Start Analysis", variant="primary", size="lg")
        
        with gr.Column(scale=2):
            status_text = gr.Textbox(
                label="Status",
                placeholder="Click 'Start Analysis' to begin...",
                lines=8
            )
    
    chart_output = gr.Image(
        label="📊 Brand Distribution Chart",
        type="filepath"
    )
    
    # Connect button to function
    submit_btn.click(
        fn=scrape_and_analyze,
        inputs=[num_images],
        outputs=[status_text, chart_output]
    )
    
    gr.Markdown("""
    ---
    ### 🎯 Supported Brands
    Audi • BMW • Lamborghini • Mercedes • Porsche • Toyota • Others
    
    Built with PyTorch and MobileNetV2 | Deployed on 🤗 Hugging Face Spaces
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch()
