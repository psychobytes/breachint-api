from flask import Blueprint
from controllers.BreachintController import search
from controllers.BreachintController import get_log_entries

breachint_bp = Blueprint('Breachint_bp', __name__)

breachint_bp.route('/api/search', methods=['POST'])(search)
breachint_bp.route('/logs', methods=['GET'])(get_log_entries)