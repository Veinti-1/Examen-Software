from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

candidates = []
voters = []
is_creation_phase_open = True
is_voting_phase_open = False

@app.route('/candidates', methods=['POST'])
def create_candidate():
    # Verificar si la fase de creación de candidatos está abierta
    if not is_creation_phase_open:
        return jsonify({'error': 'La fase de creación de candidatos está cerrada.'}), 400
    data = request.json
    # Validar que se envíen los datos necesarios del candidato
    if 'name' not in data or 'description' not in data:
        return jsonify({'error': 'El nombre y la descripción del candidato son requeridos.'}), 400
    candidate = {
        'name': data['name'],
        'description': data['description']
    }
    # Agregar el candidato a la lista de candidatos
    candidates.append(candidate)
    return jsonify({'message': 'Candidato creado exitosamente.'}), 201

@app.route('/close-creation-phase', methods=['POST'])
def close_creation_phase():
    global is_creation_phase_open
    # Cerrar la fase de creación de candidatos
    is_creation_phase_open = False
    return jsonify({'message': 'La fase de creación de candidatos ha sido cerrada.'}), 200

@app.route('/vote', methods=['POST'])
def vote():
    # Verificar si la fase de votación está abierta
    if not is_voting_phase_open:
        return jsonify({'error': 'La fase de votación está cerrada.'}), 400
    data = request.json
    # Validar que se envíen los datos necesarios del votante y el voto
    if 'voter_id' not in data or 'candidate_name' not in data:
        return jsonify({'error': 'El ID del votante y el nombre del candidato son requeridos.'}), 400
    voter_id = data['voter_id']
    candidate_name = data['candidate_name']
    # Verificar si el votante ya ha votado
    if any(voter['id'] == voter_id for voter in voters):
        return jsonify({'error': 'Este votante ya ha votado.'}), 400
    # Verificar si el candidato existe
    candidate = next((c for c in candidates if c['name'] == candidate_name), None)
    if not candidate:
        return jsonify({'error': f'El candidato {candidate_name} no existe.'}), 400
    # Agregar el voto a la lista de votantes y su voto
    voters.append({'id': voter_id})
    candidate['votes'] = candidate.get('votes', 0) + 1
    return jsonify({'message': 'Voto registrado exitosamente.'}), 201

@app.route('/close-voting-phase', methods=['POST'])
def close_voting_phase():
    global is_voting_phase_open
    # Cerrar la fase de votación
    is_voting_phase_open = False
    return jsonify({'message': 'La fase de votación ha sido cerrada.'}), 200

@app.route('/stats', methods=['GET'])
def stats():
    # Calcular estadísticas
    total_votes = sum(candidate.get('votes', 0) for candidate in candidates)
    fraud_votes = len(voters) - total_votes
    return jsonify({ 'total_votes': total_votes, 'fraud_votes': fraud_votes }), 200
