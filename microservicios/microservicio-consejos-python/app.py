import os
from flask import Flask, jsonify, redirect, send_from_directory
from pymongo import MongoClient

app = Flask(__name__)

# Conexión a MongoDB Atlas
MONGO_URI = os.environ.get('MONGO_URI')
cliente = MongoClient(MONGO_URI)
base_datos = cliente['mascotas_db']
coleccion_consejos = base_datos['consejos']

# Ruta raíz
@app.route('/')
def inicio():
    return jsonify({'mensaje': 'Microservicio de consejos para mascotas perdidas funcionando'})

# Redirección de api-docs a la raíz del servicio
@app.route('/api-docs')
def api_docs():
    return redirect("/")

# Endpoint para obtener consejos de mascotas
@app.route('/consejos')
def obtener_consejos():
    consejos = list(coleccion_consejos.find({}, {'_id': 0}))
    return jsonify(consejos)

# Archivos de documentación existentes
@app.route('/docs')
def docs():
    return send_from_directory('.', 'docs.html')

@app.route('/openapi.json')
def openapi():
    return send_from_directory('.', 'openapi.json')

# Arranque del servidor
if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=puerto)