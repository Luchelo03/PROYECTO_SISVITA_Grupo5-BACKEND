from model.provincia import Provincia
from flask import Blueprint, request, jsonify, make_response
from utils.db import db

provincia_routes=Blueprint('provincia_routes', __name__)

@provincia_routes.route('/api/provinces/<int:department_id>', methods=['GET'])
def get_provinces(department_id):
    provinces = Provincia.query.filter_by(department_id=department_id).all()
    return jsonify([{'id': p.id, 'name': p.province} for p in provinces])
