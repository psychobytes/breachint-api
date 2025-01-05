import bcrypt
from config import db
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from datetime import timedelta
from models.AdminModel import Admin

# fungsi untuk hash password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# fungsi untuk verifikasi password
def check_password_hash(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

# jwt login
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    admin = Admin.query.filter_by(username=username).first()
    if not admin or not check_password_hash(admin.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    access_token = create_access_token(identity=admin.username, expires_delta=timedelta(hours=1))
    return jsonify({'access_token': access_token})

def add_admin():
    new_admin_data = request.get_json()
    hashed_pw = hash_password(new_admin_data['password'])
    new_admin = Admin(
        username = new_admin_data['username'],
        password = hashed_pw
    )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'message': 'Admin added successfully!', 'admin': new_admin.to_dict()}), 201

def get_admins():
    admins = Admin.query.all()
    admin_data = []
    for admin in admins:
        admin_data.append({
            'id':admin.id,
            'username':admin.username,
            'password':admin.password
        })
    response = {
        'status': 'success',
        'data': {
            'admin': admin_data
        },
        'message': 'Admin retrieved successfully'
    }
    return jsonify(response), 200