from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from .logic import register_user, login_user

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    result = register_user(
        data.get('username', ''),
        data.get('email', ''),
        data.get('password', '')
    )

    if not result["ok"]:
        return jsonify({"status": "error", "message": result["error"]}), 400

    return jsonify(
        {
            "status": "success",
            "message": result["message"],
            "user_id": result["user_id"]
        }
    ), 201


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    result = login_user(
        data.get('username', ''),
        data.get('email', ''),
        data.get('password', '')
    )

    if not result["ok"]:
        return jsonify({"status": "error", "message": result["error"]}), 401

    user = result["user"]
    access_token = create_access_token(
        identity=user["id"],
        additional_claims={
            "username": user["username"],
            "email": user["email"],
        },
    )

    return jsonify(
        {
            "status": "success",
            "message": result["message"],
            "user": user,
            "access_token": access_token,
        }
    ), 200


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    claims = get_jwt()
    return jsonify(
        {
            "status": "success",
            "user": {
                "id": get_jwt_identity(),
                "username": claims.get("username", ""),
                "email": claims.get("email", ""),
            },
        }
    ), 200
