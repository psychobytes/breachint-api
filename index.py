from config import app, db
from routes.User_bp import user_bp
from routes.Admin_bp import admin_bp
from routes.Breachint_bp import breachint_bp
from flask import request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# Untuk menangani dokumentasi API dengan Flask-RESTX
from flask_restx import Api, Resource, fields
from controllers.AdminController import admin_required, hash_password, check_password_hash
from models.UserModel import User
from datetime import timedelta

# Inisialisasi Flask-JWT Manager
jwt = JWTManager(app)

# Register Blueprints untuk routes yang sudah ada
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(breachint_bp)

# Endpoint root
@app.route("/")
def home():
    return "Breachint API"

# Exclude routes dari pengecekan autentikasi
@app.before_request
def before_request():
    excluded_routes = ['/admin/login', '/admin/register', '/user/login', '/user/register']
    if request.path in excluded_routes:
        return None
    return None

# Endpoint untuk mengakses fitur protected dengan JWT
@app.route("/admin/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

def auth_header():
    return {'Authorization': {'description': 'JWT Token', 'in': 'header', 'type': 'string', 'required': True}}

# Setup Flask-RESTX untuk API Dokumentasi
api = Api(app, version="1.0", title="Breachint API", description="A secure API for managing users.", doc="/swagger")

# Models untuk dokumentasi API
user_model = api.model('User', {
    'username': fields.String(required=True, description='The user username'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
})

# Model untuk dokumentasi input admin
admin_model = api.model('Admin', {
    'username': fields.String(required=True, description='The admin username'),
    'password': fields.String(required=True, description='The admin password'),
    'admin_token': fields.String(required=True, description='The admin token'),
    'role': fields.String(required=False, description='The admin role (default: administrator)')
})

# Namespace untuk user & admin routes
user_ns = api.namespace('user', description='User operations')
admin_ns = api.namespace('admin', description='Admin operations')

# Login user dan menghasilkan JWT
@user_ns.route('/login')
class UserLogin(Resource):
    @api.doc(body=user_model)
    def post(self):
        """
        Login user, mengembalikan token JWT
        """
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        access_token = create_access_token(identity=user.email, expires_delta=timedelta(hours=1))
        return jsonify({'access_token': access_token})

# Register user baru
@user_ns.route('/register')
class UserRegister(Resource):
    @api.doc(body=user_model)
    def post(self):
        """
        Registrasi user baru
        """
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

#Mendapatkan user berdasarkan ID 
@admin_ns.route('/users/<int:user_id>')
class GetUser(Resource):
    @admin_required
    @api.doc(params={**auth_header(), 'user_id': 'The ID of the user'})
    def get(self, user_id):
        """
        Mendapatkan user berdasarkan ID (hanya admin)
        """
        user = User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        user_data = {'id': user.id, 'username': user.username, 'email': user.email}
        response = {
            'status': 'success',
            'data': user_data,
            'message': 'User retrieved successfully'
        }
        return jsonify(response), 200

# Mendapatkan semua user
@admin_ns.route('/users')
class GetAddUsers(Resource):
    @admin_required
    @api.doc(params=auth_header())
    def get(self):
        """
        Mendapatkan daftar semua user (hanya admin)
        """
        users = User.query.all()
        user_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        response = {
            'status': 'success',
            'data': user_data,
            'message': 'Users retrieved successfully'
        }
        return jsonify(response), 200

    @admin_required
    @api.expect(user_model)
    @api.doc(params=auth_header())
    def post(self):
        """
        Menambahkan user baru (hanya admin)
        """
        new_user_data = request.get_json()
        hashed_pw = hash_password(new_user_data['password'])
        new_user = User(
            username=new_user_data['username'],
            email=new_user_data['email'],
            password=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully!', 'user': new_user.to_dict()}), 201

# Update user berdasarkan ID
@admin_ns.route('/users/<int:user_id>')
class UpdateDeleteUser(Resource):
    @admin_required
    @api.expect(user_model)
    @api.doc(params={**auth_header(), 'user_id': 'The ID of the user'})
    def put(self, user_id):
        """
        Update user berdasarkan ID (hanya admin)
        """
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        updated_data = request.get_json()
        user.username = updated_data.get('username', user.username)
        user.email = updated_data.get('email', user.email)
        user.password = hash_password(updated_data['password']) if 'password' in updated_data else user.password

        db.session.commit()
        return jsonify({'message': 'User updated successfully!', 'user': user.to_dict()}), 200
    
    @admin_required
    @api.doc(params={**auth_header(), 'user_id': 'The ID of the user'})
    def delete(self, user_id):
        """
        Menghapus user berdasarkan ID (hanya admin)
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            db.session.delete(user)
            db.session.commit()
            
            return {'message': 'User deleted successfully!'}, 200
        
        except Exception as e:
            return {'error': str(e)}, 500

# Login admin
@admin_ns.route('/login')
class AdminLogin(Resource):
    @api.doc(body=admin_model)
    def post(self):
        """
        Login admin, mengembalikan token JWT
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        admin = Admin.query.filter_by(username=username).first()
        if not admin or not check_password_hash(admin.password, password):
            return jsonify({'message': 'Invalid username or password'}), 401

        access_token = create_access_token(identity=admin.username, expires_delta=timedelta(hours=1))
        return jsonify({'access_token': access_token}), 200

# Registrasi Admin Baru
@admin_ns.route('/register')
class AdminRegister(Resource):
    @api.expect(admin_model)
    def post(self):
        """
        Registrasi admin baru
        """
        data = request.get_json()
        admin_token = data.get('admin_token')
        
        if not admin_token:
            return jsonify({'message': 'Admin token is required in the payload'}), 400
        if admin_token != app.config['ADMIN_TOKEN']:
            return jsonify({'message': 'Unauthorized: Invalid admin token'}), 403

        username = data.get('username')
        password = data.get('password')

        if Admin.query.filter_by(username=username).first():
            return jsonify({'message': 'Admin username already exists'}), 400

        new_admin = Admin(
            username=username,
            password=hash_password(password),
            role=data.get('role', 'administrator') 
        )
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({'message': 'Admin registered successfully!'}), 201

    
# Mendapatkan daftar admin
@admin_ns.route('/view-admin')
class ViewAdmins(Resource):
    @admin_required
    @api.doc(params={'Authorization': {'description': 'JWT Token', 'in': 'header', 'type': 'string', 'required': True}})
    def get(self):
        """
        Mendapatkan daftar semua admin (hanya untuk admin)
        """
        admins = Admin.query.all()
        admin_list = [{'id': admin.id, 'username': admin.username, 'role': admin.role} for admin in admins]

        return jsonify({
            'status': 'success',
            'data': admin_list,
            'message': 'Admins retrieved successfully'
        }), 200

# Menambahkan namespace ke API
api.add_namespace(user_ns)
api.add_namespace(admin_ns)

if __name__ == '__main__':
    db.create_all() 
    app.run(debug=True)
