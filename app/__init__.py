from flask import Flask
from .routes import bp

import os

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, '..', 'templates')
    app = Flask(__name__, template_folder=template_dir)
    app.register_blueprint(bp)
    return app

