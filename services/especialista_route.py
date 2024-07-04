from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from model.usuario import Usuario
from model.persona import Persona
from model.codigos_unicos import Codigos
from model.especialista import Especialista
from schemas.especialista_schema import especialista_schema


especialista_routes=Blueprint('especialista_routes', __name__)

@especialista_routes.route('/especialista/add', methods=['POST'])
def create_Especialista():
    try:
        # Extraer datos del JSON
        email = request.json['email']
        password = request.json['password']
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        specialty = request.json['specialty']
        code = request.json['codigo_especialista']
        cell_phone = request.json['cell_phone']  # Nuevo campo: número de celular
        department_id = request.json['department_id']  # Nuevo campo: ID de departamento
        province_id = request.json['province_id']  # Nuevo campo: ID de provincia
        district_id = request.json['district_id']  # Nuevo campo: ID de distrito

        # Verificar si el email ya existe
        if Usuario.query.filter_by(email=email).first():
            return jsonify({'message': 'El email ya está registrado'}), 400

        # Crear un nuevo usuario
        new_user = Usuario(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Crear una nueva persona asociada al usuario
        new_person = Persona(first_name=first_name, last_name=last_name, role='Especialista', user_id=new_user.id, 
                             cell_phone=cell_phone, department_id=department_id, province_id=province_id, 
                             district_id=district_id)
        db.session.add(new_person)
        db.session.commit()

        # Crear una nueva entrada en unique_codes
        new_code = Codigos(code=code)
        db.session.add(new_code)
        db.session.commit()

        # Crear un nuevo 
        new_specialist = Especialista(person_id=new_person.id, codigo_especialista=code, specialty=specialty)
        db.session.add(new_specialist)
        db.session.commit()
        
        data = {
            'message': 'Especialista creado con éxito',
            'status': 200,
            'especialista': especialista_schema.dump(new_specialist)
        }
        return make_response(jsonify(data), 200)
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error al crear el especialista, posiblemente el código o el email ya existen'}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear el especialista: {str(e)}'}), 500


@especialista_routes.route('/especialista/buscarPorEmail', methods=['GET'])
def get_specialist_by_email():
    email = request.args.get('email')
    if not email:
        return jsonify({'message': 'Email is required'}), 400

    user = Usuario.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    person = Persona.query.filter_by(user_id=user.id).first()
    if not person:
        return jsonify({'message': 'Person not found'}), 406

    specialist = Especialista.query.filter_by(person_id=person.id).first()
    if not specialist:
        return jsonify({'message': 'Specialist not found'}), 407
    

    result = {}
    result["data"]=[
        {
        'id': specialist.id,
        'first_name': specialist.person.first_name,
        'last_name': specialist.person.last_name,
        'email': user.email,
        'specialist_code': specialist.codigo_especialista,
        'specialty': specialist.specialty,
        'rol': specialist.person.role,
        }
    ]

    return jsonify(result), 200
