from flask import Blueprint
from controllers.BreachintController import search

breachint_bp = Blueprint('Breachint_bp', __name__)

breachint_bp.route('/api/search', methods=['GET'])(search)