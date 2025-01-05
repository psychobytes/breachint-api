from flask import jsonify, request
from models.UserModel import User
from config import db
from flask_jwt_extended import jwt_required

@jwt_required()
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

@jwt_required()
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

@jwt_required()
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

@jwt_required()
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

@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})