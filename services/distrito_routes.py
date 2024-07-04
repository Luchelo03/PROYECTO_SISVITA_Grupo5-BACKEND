from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from model.distrito import Distrito

distrito_routes=Blueprint('distrito_routes', __name__)

@distrito_routes.route('/api/districts/<int:province_id>', methods=['GET'])
def get_districts(province_id):
    districts = Distrito.query.filter_by(province_id=province_id).all()
    return jsonify([{'id': d.id, 'name': d.district} for d in districts])
