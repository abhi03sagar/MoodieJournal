# backend/extensions.py
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# We create the instances here, but we don't attach them to the 'app' yet.
mongo = PyMongo()
jwt = JWTManager()
bcrypt = Bcrypt()