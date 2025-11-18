"""
Main entry point for the Flask application
"""

from app.routes import app
import os

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/raw_images', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Get port from environment (for deployment) or use 5001 locally
    port = int(os.environ.get('PORT', 5001))
    
    # Run the Flask app
    print("\n" + "="*50)
    print("🚗 Car Brand Detection System")
    print("="*50)
    print("Starting server...")
    print(f"Open http://127.0.0.1:{port}/ in your browser")
    print("="*50 + "\n")
    
    # Use 0.0.0.0 for deployment, debug=False in production
    app.run(debug=False, host='0.0.0.0', port=port)

