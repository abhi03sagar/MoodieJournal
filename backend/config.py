import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # 1. Load from .env (No hardcoded defaults for secrets!)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
    
    # 2. Match the key name exactly as it is in your .env file
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    
    PORT = 5000
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)