from flask import Flask, jsonify
from app.extensions import db, jwt, migrate
from app.config import Config
from app.routes.main import main_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    @app.route('/')
    def home():
        return jsonify({"message": "Flask API is running!"})

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_blueprint)

    return app
