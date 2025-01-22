import bcrypt
from config import db, app
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from datetime import timedelta
from models.AdminModel import Admin

from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps

# fungsi untuk hash password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# fungsi untuk verifikasi password
def check_password_hash(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def admin_required(fn):
    @wraps(fn)  # Preserve the original function's name and docstring
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if 'role' not in claims:
            return jsonify({"msg": "Admin access required"}), 403
        if claims['role'] != 'administrator':
            return jsonify({"msg": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

# jwt login
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    admin = Admin.query.filter_by(username=username).first()
    if not admin or not check_password_hash(admin.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    additional_claims = {"role": admin.role}

    access_token = create_access_token(identity=admin.username, additional_claims=additional_claims, expires_delta=timedelta(hours=1))
    return jsonify({'access_token': access_token})


def add_admin():
    data = request.get_json()
    admin_token = data.get('admin_token')

    if not admin_token:
        return jsonify({'message': 'Admin token is required in the payload'}), 400
    if admin_token != app.config['ADMIN_TOKEN']:
        return jsonify({'message': 'Unauthorized: Invalid admin token'}), 403
    
    username = data.get('username')
    password = data.get('password')
    hashed_pw = hash_password(password)

    if Admin.query.filter_by(username=username).first():
        return jsonify({'message': 'Admin username already exists'}), 400
    new_admin = Admin(
        username=username,
        password=hashed_pw
    )
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({'message': 'Admin added successfully!', 'admin': new_admin.to_dict()}), 201


@admin_required
def get_admins():
    admins = Admin.query.all()
    admin_data = []
    for admin in admins:
        admin_data.append({
            'id':admin.id,
            'username':admin.username,
            'password':admin.password,
            'role':admin.role
        })
    response = {
        'status': 'success',
        'data': {
            'admin': admin_data
        },
        'message': 'Admin retrieved successfully'
    }
    return jsonify(response), 200