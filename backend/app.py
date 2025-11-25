from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config
from extensions import mongo, jwt, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    mongo.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # CORS (Equivalent to your cors setup)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

    # Import and Register Blueprints (Routes)
    from routes.auth import auth_bp
    from routes.entries import entries_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(entries_bp, url_prefix="/api/entries")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=Config.PORT)