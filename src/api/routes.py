"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from flask_bcrypt import Bcrypt

api = Blueprint('api', __name__)

bcrypt = Bcrypt()
jwt = JWTManager()

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 409

    # Hash password
    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    # Create new user
    new_user = User(email=email, password=hashed_pw, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    # Generate JWT token
    access_token = create_access_token(identity=new_user.id)

    return jsonify({
        "msg": "Signup successful",
        "access_token": access_token,
        "user": {
            "id": new_user.id,
            "email": new_user.email
        }
    }), 201


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    # Look up the user
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Verify password
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=user.id)

    return jsonify({
        "msg": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email
        }
    }), 200

