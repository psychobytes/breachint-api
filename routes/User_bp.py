from flask import Blueprint
from controllers.UserController import get_users, get_user, add_user, update_user, delete_user, login, register

user_bp = Blueprint('User_bp', __name__)

user_bp.route('/admin/users', methods=['GET'])(get_users)
user_bp.route('/admin/users/<int:user_id>', methods=['GET'])(get_user)
user_bp.route('/admin/users', methods=['POST'])(add_user)
user_bp.route('/admin/users/<int:user_id>', methods=['PUT'])(update_user)
user_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])(delete_user)

user_bp.route('/user/login', methods=['POST'])(login)
user_bp.route('/user/register', methods=['POST'])(register)