from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from model.usuario import Usuario
from schemas.usuario_schema import usuarios_schema, usuario_schema

usuario_routes = Blueprint('usuario_routes', __name__)

@usuario_routes.route('/usuario/listar', methods={'GET'})
def get_usuario():
    all_usuarios = Usuario.query.all()
    result = usuarios_schema.dump(all_usuarios)
    data = {
        'message': 'Todas las filas de la tabla usuario recuperadas',
        'status': 200,
        'data': result
    }
    
    return make_response(jsonify(data), 200)

@usuario_routes.route('/usuario', methods=['POST'])
def create_Usuario():
    
    email = request.json.get('email')
    password = request.json.get('password')
    
    if not email or not password:
        return make_response(jsonify({'message': 'Email y contraseña son requeridos', 'status': 400}), 400)
    
    new_usuario = Usuario(email, password)
    
    db.session.add(new_usuario)
    db.session.commit()
    
    result = usuario_schema.dump(new_usuario)
    
    data={
        'message': 'Nuevo usuario ingresado correctamente',
        'status': 201,
        'data': result
    }
    
    return make_response(jsonify(data),201)

@usuario_routes.route('/usuario/delete', methods=['DELETE'])
def delete():
    
    result = {}
    body = request.get_json()
    id = body.get('id')
    
    if id is None:
        return jsonify({"error": "Falta el id en el body"}), 400
    
    usuario = Usuario.query.get(id)
    if usuario is None:
        return jsonify({"error": f"Usuario con id {id} no fue hallado"}), 404
    
    db.session.delete(usuario)
    db.session.commit()
    
    result["data"]=usuario
    result["status_code"]=200
    result["msg"]="Se eliminó el usuario"
    
    return jsonify(result), 200

@usuario_routes.route('/usuario/update', methods=['POST'])
def update():
    
    result = {}
    body = request.get_json()
    id = body.get('id')
    email = body.get('email')
    password = body.get('password')
    
    if not email or not password:
        return jsonify({'error': 'email y password se requieren'}), 400
    
    usuario = Usuario.query.get(id)
    
    if usuario is None:
        return jsonify({"error": f"Usuario con id {id} no fue encontrado"}),404
    
    usuario.id = id
    usuario.email = email
    
    passworda = usuario.hash_password(password)
    
    usuario.password = passworda
    
    db.session.commit()
    
    result["data"] = usuario
    result["status_code"] = 202
    result["msg"] = "Se modificó el usuario sin convenientes"
    
    return jsonify(result), 202