from flask import jsonify, request
from models.UserModel import User
from config import db
from flask_jwt_extended import jwt_required

from flask_jwt_extended import create_access_token
from datetime import timedelta

# import fungsi jwt verif role admin
from controllers.AdminController import admin_required

# import fungsi bikin hash & verif hash password
from controllers.AdminController import hash_password, check_password_hash

# user login (get jwt token)
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=user.email, expires_delta=timedelta(hours=1))
    return jsonify({'access_token': access_token})

# register user
def register():
    new_user_data = request.get_json()
    hashed_pw = hash_password(new_user_data['password'])
    new_user = User(
        username = new_user_data['username'],
        email = new_user_data['email'],
        password = hashed_pw
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!', 'user': new_user.to_dict()}), 201

@admin_required
def get_users():
    users = User.query.all()
    user_data = []
    for user in users:
        user_data.append({
            'id':user.id,
            'username':user.username,
            'password':user.password
        })
    response = {
        'status': 'success',
        'data': {
            'user': user_data
        },
        'message': 'User retrieved successfully'
    }
    return jsonify(response), 200

@admin_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password': user.password
    }
    response = {
        'status': 'success',
        'data': {
            'user': user_data
        },
        'message': 'User retrieved successfully'
    }
    return jsonify(response), 200

@admin_required
def add_user():
    new_user_data = request.get_json()
    new_user = User(
        username=new_user_data['username'],
        email=new_user_data['email'],
        password=new_user_data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully!', 'user': new_user.to_dict()}), 201

@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    updated_data = request.get_json()
    user.username = updated_data.get('title', user.username)
    user.email= updated_data.get('author', user.email)
    user.password = updated_data.get('year', user.password)

    db.session.commit()
    return jsonify({'message': 'User updated successfully!', 'user': user.to_dict()})

@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})