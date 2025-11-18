from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_images():
    """
    Step 1: Scrape images from the web
    Receives: { "count": number_of_images }
    Returns: { "status": "done", "images_scraped": count }
    """
    try:
        data = request.get_json()
        image_count = data.get('count', 50)
        
        # Validate input
        if image_count < 10 or image_count > 200:
            return jsonify({
                'status': 'error',
                'error': 'Image count must be between 10 and 200'
            })
        
        # Import scraper function
        from scripts.scrapper import scrape_flickr_simple
        
        # Scrape images
        images_scraped = scrape_flickr_simple(
            url="https://www.flickr.com/groups/carexpressions/pool/",
            save_dir="static/raw_images",
            limit=image_count
        )
        
        if images_scraped == 0:
            return jsonify({
                'status': 'error',
                'error': 'No images could be scraped. Please try again.'
            })
        
        return jsonify({
            'status': 'done',
            'images_scraped': images_scraped
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

@app.route('/analyze', methods=['POST'])
def analyze_images():
    """
    Step 2: Analyze scraped images and generate chart
    Returns: { "status": "done" }
    """
    try:
        # Check if images exist
        raw_images_dir = "static/raw_images"
        if not os.path.exists(raw_images_dir) or len(os.listdir(raw_images_dir)) == 0:
            return jsonify({
                'status': 'error',
                'error': 'No images found. Please scrape images first.'
            })
        
        # Import prediction and visualization functions
        from app.predictor import predict_brands
        from visualize.plot import create_brand_chart
        
        # Run predictions on scraped images
        brand_counts = predict_brands(raw_images_dir)
        
        if not brand_counts:
            return jsonify({
                'status': 'error',
                'error': 'Could not detect any brands in the images.'
            })
        
        # Generate chart
        chart_path = "static/brand_chart.png"
        create_brand_chart(brand_counts, chart_path)
        
        return jsonify({
            'status': 'done',
            'brands_detected': len(brand_counts)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
