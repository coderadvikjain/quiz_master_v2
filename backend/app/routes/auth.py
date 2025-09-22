from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.model.models import User, db
import os
from app import limiter
from datetime import datetime

auth = Blueprint('auth', __name__)

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@StudiQ.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin@123")

# -------- SIGNUP --------

@limiter.limit("10 per day") 
@auth.post('/register')
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'User already exists'}), 409

    dob_str = data.get('dob')
    dob_date = None
    if dob_str:
        try:
            dob_date = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'msg': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    hashed_password = generate_password_hash(data['password'])
    user = User(
        email=data['email'],
        password=hashed_password,
        full_name=data['full_name'],
        qualification=data.get('qualification'),
        dob=dob_date)
    
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'User registered successfully'}), 201

# -------- AUTH --------

@limiter.limit("5 per minute")
@auth.post('/login')
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        token = create_access_token(identity=email, additional_claims={'role': 'admin'})
        return jsonify({'access_token': token, 'role': 'admin'}), 200

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'msg': 'Invalid credentials'}), 401

    token = create_access_token(identity=str(user.id), additional_claims={'role': 'user','full_name': user.full_name})
    return jsonify({'access_token': token, 'role': 'user'}), 200