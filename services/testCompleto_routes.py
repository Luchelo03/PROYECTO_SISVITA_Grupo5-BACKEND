import pprint
from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from model.test import Test
from model.pregunta import Pregunta
from model.opcion import Opcion
from model.diagnostico import Diagnostico
from model.resultado import Result
from model.semaforo import Semaforo
from datetime import datetime

test_routes = Blueprint('test_routes', __name__)

@test_routes.route('/test/new', methods=['POST'])
def create_test():
    data = request.get_json()
    
    # Crear el test
    new_test = Test(test_name=data['test_name'])
    db.session.add(new_test)
    db.session.commit()
    
    # Crear las preguntas y opciones
    for question_data in data['questions']:
        new_question = Pregunta(test_id=new_test.id, question_text=question_data['question_text'])
        db.session.add(new_question)
        db.session.commit()
        
        for option_data in question_data['options']:
            new_option = Opcion(question_id=new_question.id, option_text=option_data['option_text'], score=option_data['score'])
            db.session.add(new_option)
    
    db.session.commit()
    
    return make_response(jsonify({
        'message': 'Se creó exitosamente el Test',
        'status': 201,
        'data': {
            'test_id': new_test.id,
            'test_name': new_test.test_name
        }
    }), 201)

"""
@test_routes.route('/test/submit_test', methods=['POST'])
def submit_test():
    data = request.get_json()
    codigo_entidad = data['codigo_entidad']
    test_id = data['test_id']
    answers = data['answers']
    
    #codigo_entidad = request.get_json('codigo_entidad')
    #test_id = request.get_json('test_id')
    #answers = request.get_json('answers')

    total_score = 0
    for answer in answers:
        option_id = int(answer['option_id'])
        option = Opcion.query.filter_by(id=option_id).first()
        if option:
            total_score += option.score
        
    #para el test de zung
    total_score=(total_score/80)*100
    print("puntuacion final:",total_score)
    
    diagnosis = Diagnostico.query.filter(
        Diagnostico.test_id == test_id,
        Diagnostico.min_score <= total_score,
        Diagnostico.max_score >= total_score
    ).first()

    if diagnosis:
        new_result = Result(
            codigo_entidad=codigo_entidad,
            test_id=test_id,
            total_score=total_score,
            diagnosis_id=diagnosis.id,
            created_at=datetime.now()  # Asegúrate de establecer la fecha y hora actuales
        )
        db.session.add(new_result)
        db.session.commit()

        return jsonify({
            'total_score': total_score,
            'diagnosis': diagnosis.diagnosis_text
        }), 200
    else:
        return jsonify({
            'message': 'Diagnostico not found for the given score'
        }), 400  """
        
@test_routes.route('/test/submit_test', methods=['POST'])
def submit_test():
    try:
        data = request.get_json()
        codigo_entidad = data['codigo_entidad']
        test_id = data['test_id']
        answers = data['answers']

        total_score = 0
        for answer in answers:
            option_id = int(answer['option_id'])
            option = Opcion.query.filter_by(id=option_id).first()
            if option:
                total_score += option.score
        
        # Calcular la puntuación total para el test de Zung
        total_score = (total_score / 80) * 100
        print("Puntuación final:", total_score)
        
        # Obtener el diagnóstico basado en la puntuación
        diagnosis = Diagnostico.query.filter(
            Diagnostico.test_id == test_id,
            Diagnostico.min_score <= total_score,
            Diagnostico.max_score >= total_score
        ).first()

        if not diagnosis:
            return jsonify({'message': 'Diagnostico no hallado para el score obtenido'}), 400

        # Determinar el semáforo basado en el diagnóstico
        semaforo = None
        if diagnosis.diagnosis_text == 'Dentro de los límites normales. No hay ansiedad presente.':
            semaforo = Semaforo.query.filter_by(color='verde').first()
        elif diagnosis.diagnosis_text == '"Presencia de ansiedad mínima moderada."':
            semaforo = Semaforo.query.filter_by(color='ambar').first()
        elif diagnosis.diagnosis_text in ['Presencia de ansiedad en grado máximo.', 'Presencia de ansiedad marcada a severa.']:
            semaforo = Semaforo.query.filter_by(color='rojo').first()

        if not semaforo:
            return jsonify({'message': 'Semaforo no hallado para el diagnostico'}), 400

        # Crear un nuevo resultado
        new_result = Result(
            codigo_entidad=codigo_entidad,
            test_id=test_id,
            total_score=total_score,
            diagnosis_id=diagnosis.id,
            semaforo_id=semaforo.id,
            created_at=datetime.now()  # Establecer la fecha y hora actuales
        )
        db.session.add(new_result)
        db.session.commit()

        return jsonify({
            'total_score': total_score,
            'diagnosis': diagnosis.diagnosis_text,
            'semaforo': semaforo.color
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al procesar el test: {str(e)}'}), 500

        
@test_routes.route('/test/get_questions', methods=['GET'])
def get_questions():
    test_id = 1  # Asumiendo que solo hay un test o especifica el test_id necesario
    test = Test.query.filter_by(id=test_id).first()

    if not test:
        return jsonify({'message': 'Test not found'}), 404


    questions = Pregunta.query.filter_by(test_id=test.id).all()
    question_list = []

    for question in questions:
        options = Opcion.query.filter_by(question_id=question.id).all()
        option_list = [{'id': option.id, 'text': option.option_text, 'score': option.score} for option in options]
        question_list.append({'id': question.id, 'text': question.question_text, 'options': option_list})

    return jsonify({'test_name': test.test_name, 'questions': question_list})