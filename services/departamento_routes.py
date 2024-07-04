from model.department import Departamentos
from flask import Blueprint, request, jsonify, make_response
from utils.db import db

departamento_routes=Blueprint('departamento_routes', __name__)

@departamento_routes.route('/api/departments', methods=['GET'])
def get_departments():
    departments = Departamentos.query.all()
    return jsonify([{'id': d.id, 'name': d.department} for d in departments])
