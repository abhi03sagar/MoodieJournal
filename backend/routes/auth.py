from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, 
    get_jwt_identity, get_jwt, decode_token
)
from bson import ObjectId
from extensions import mongo, bcrypt

auth_bp = Blueprint('auth', __name__)

# Simulating your in-memory refresh token list (Note: Redis is better for production)
refresh_tokens_store = []

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing credentials"}), 400

    users_col = mongo.db.users
    if users_col.find_one({"username": username}):
        return jsonify({"message": "Username taken"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_id = users_col.insert_one({"username": username, "password": hashed_password}).inserted_id

    # Generate Tokens
    # Note: We convert ObjectId to string for the token payload
    access_token = create_access_token(identity=str(user_id))
    refresh_token = create_refresh_token(identity=str(user_id))
    
    refresh_tokens_store.append(refresh_token)

    # Set Cookie and Response
    resp = make_response(jsonify({"accessToken": access_token, "username": username}))
    resp.set_cookie('refreshToken', refresh_token, httponly=True, samesite='Strict', max_age=7*24*60*60)
    
    return resp, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"message": "Invalid Username"}), 401

    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Incorrect password"}), 401

    access_token = create_access_token(identity=str(user['_id']))
    refresh_token = create_refresh_token(identity=str(user['_id']))
    
    refresh_tokens_store.append(refresh_token)

    resp = make_response(jsonify({"accessToken": access_token, "username": username}))
    resp.set_cookie('refreshToken', refresh_token, httponly=True, samesite='Strict', max_age=7*24*60*60)
    
    return resp

@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    # In Flask, we can grab the cookie manually or use jwt_extended features
    token = request.cookies.get('refreshToken')
    
    if not token:
        return jsonify({"message": "No refresh token provided"}), 401
    
    if token not in refresh_tokens_store:
        return jsonify({"message": "Invalid refresh token"}), 403

    # Verify and decode manually to handle custom logic if needed, 
    # or rely on jwt_extended decorators. Here is a manual verify approach:
    try:
        # We need to decode it to get the user ID. 
        # In a real app, use @jwt_required(refresh=True)
        decoded = decode_token(token)
        new_access_token = create_access_token(identity=decoded['sub']) # 'sub' is the identity
        return jsonify({"accessToken": new_access_token})
    except Exception:
        return jsonify({"message": "Expired or invalid refresh token"}), 403

@auth_bp.route('/logout', methods=['POST'])
def logout():
    token = request.cookies.get('refreshToken')
    if token and token in refresh_tokens_store:
        refresh_tokens_store.remove(token)
    
    resp = make_response(jsonify({"message": "Logged out successfully"}))
    resp.set_cookie('refreshToken', '', expires=0)
    return resp