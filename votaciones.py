import json
import os
import dapr
from flask import Flask, request, jsonify

# Crear una instancia de Flask
app = Flask(__name__)

# Definir la ruta y método HTTP del endpoint que permite crear candidatos
@app.route('/candidatos', methods=['POST'])
def crear_candidato():
    # Verificar si el sistema está en la fase de crear candidatos
    if Estado().obtener_estado() == 'creando_candidatos':
        # Obtener el cuerpo de la solicitud HTTP
        data = request.get_json()
        # Validar que la solicitud tenga el campo "nombre" del candidato
        if 'nombre' not in data:
            return jsonify({'error': 'Falta el campo "nombre" en la solicitud'}), 400
        # Validar que el candidato no exista en la lista de candidatos
        candidatos = Candidatos().obtener_candidatos()
        if any(c['nombre'] == data['nombre'] for c in candidatos):
            return jsonify({'error': f'El candidato "{data["nombre"]}" ya existe'}), 400
        # Agregar el candidato a la lista de candidatos
        candidatos.append(data)
        Candidatos().guardar_candidatos(candidatos)
        return jsonify({'mensaje': f'Se ha creado el candidato "{data["nombre"]}"'}), 201
    else:
        return jsonify({'error': 'El sistema no está en la fase de crear candidatos'}), 400

# Obtener el estado del sistema desde Dapr
@dapr.actor('estado')
class Estado:
    def obtener_estado(self):
        with open('estado.txt', 'r') as f:
            return f.read().strip()

# Obtener la lista de candidatos desde Dapr
@dapr.actor('candidatos')
class Candidatos:
    def obtener_candidatos(self):
        with open('candidatos.json', 'r') as f:
            return json.load(f)

    def guardar_candidatos(self, candidatos):
        with open('candidatos.json', 'w') as f:
            json.dump(candidatos, f)

if __name__ == '__main__':
    # Obtener el puerto en el que se debe ejecutar el servidor Flask
    port = int(os.environ.get('PORT', 5000))
    # Iniciar el servidor Flask
    app.run(port=port, debug=True)
