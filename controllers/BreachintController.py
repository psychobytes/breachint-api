from flask import jsonify, request
from flask_jwt_extended import jwt_required

@jwt_required()
def search():
    return "BreachInt"