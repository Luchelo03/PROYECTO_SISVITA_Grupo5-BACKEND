from flask import Blueprint, request, jsonify
from model.resultado import Result
from model.test import Test
from model.diagnostico import Diagnostico
from model.estudiante import Estudiante
from model.persona import Persona
from model.semaforo import Semaforo
from model.usuario import Usuario
from model.distrito import Distrito
from utils.db import db

resultados_routes = Blueprint('resultados_routes', __name__)

@resultados_routes.route('/resultados/<codigo_entidad>', methods=['GET'])
def get_resultados_by_codigo_entidad(codigo_entidad):
    resultados = Result.query.filter_by(codigo_entidad=codigo_entidad).all()
    if not resultados:
        return jsonify({'message': 'No hay resultados para este estudiante'}), 404

    resultados_data = []
    for resultado in resultados:
        test = Test.query.filter_by(id=resultado.test_id).first()
        diagnostico = Diagnostico.query.filter_by(id=resultado.diagnosis_id).first()

        resultados_data.append({
            'id': resultado.id,
            'fecha': resultado.created_at,
            'puntaje': resultado.total_score,
            'test_id': resultado.test_id,
            'test_name': test.test_name if test else 'Test no encontrado',
            'diagnosis_id': resultado.diagnosis_id,
            'diagnosis_text': diagnostico.diagnosis_text if diagnostico else 'Diagnóstico no encontrado'
        })

    return jsonify(resultados_data), 200


"""
@resultados_routes.route('/resultados/all', methods=['GET'])
def get_resultados_by_codigo_entidad():
    resultados = Result.query.filter_by().all()
    if not resultados:
        return jsonify({'message': 'No hay resultados para este estudiante'}), 404

    resultados_data = []
    for resultado in resultados:
        test = Test.query.filter_by(id=resultado.test_id).first()
        diagnostico = Diagnostico.query.filter_by(id=resultado.diagnosis_id).first()

        resultados_data.append({
            'id': resultado.id,
            'fecha': resultado.created_at,
            'puntaje': resultado.total_score,
            'test_id': resultado.test_id,
            'test_name': test.test_name if test else 'Test no encontrado',
            'diagnosis_id': resultado.diagnosis_id,
            'diagnosis_text': diagnostico.diagnosis_text if diagnostico else 'Diagnóstico no encontrado'
        })

    return jsonify(resultados_data), 200"""