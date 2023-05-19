import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here

    from app.train import bp as train_bp
    app.register_blueprint(train_bp)

    from app.correction import bp as correction_bp
    app.register_blueprint(correction_bp)
    
    return app