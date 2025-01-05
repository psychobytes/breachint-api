from config import app, db
from routes.User_bp import user_bp
from routes.Admin_bp import admin_bp
from flask import request, jsonify
from models.AdminModel import Admin
from controllers.AdminController import check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

jwt = JWTManager(app)

app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

@app.route("/")
def home():
    return "Breachint"

@app.before_request
def before_request():
    # daftar endpoint yang dikecualikan dari auth
    excluded_routes = ['/admin/login', '/admin/register']
    if request.path in excluded_routes:
        return None # skip auth
    
    return None

@app.route("/admin/protected", methods = ["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# comment this if want deploy to vercel
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)