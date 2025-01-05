from flask import Blueprint
from controllers.AdminController import login, add_admin, get_admins

admin_bp = Blueprint('Admin_bp', __name__)

admin_bp.route('/admin/register', methods=['POST'])(add_admin)
admin_bp.route('/admin/view-admin', methods=['GET'])(get_admins)
admin_bp.route('/admin/login', methods=['POST'])(login)