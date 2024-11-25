from flask import Flask, jsonify
from app.extensions import db, jwt, migrate
from app.config import Config
from app.routes.main import main_blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    @app.route('/')
    def home():
        return jsonify({"message": "Flask API is running!"})

    # Allow CORS requests from your frontend origin
    CORS(app, origins=["http://localhost:3000", "https://demo.tysindia.com"])

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_blueprint)

    return app
