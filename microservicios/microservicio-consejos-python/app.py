import os
from flask import Flask, jsonify, redirect
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
cliente = MongoClient(MONGO_URI) if MONGO_URI else None

@app.route('/')
def inicio():
    return jsonify({'mensaje': 'Microservicio de consejos para mascotas perdidas funcionando'})

# Redirección directa a SwaggerHub
@app.route('/api-docs')
def api_docs():
    return redirect("https://app.swaggerhub.com/apis-docs/uninpahu-b8e/microservicio-consejos-python/1.0.0", code=302)

@app.route('/consejos')
def obtener_consejos():
    if not cliente:
        return jsonify([])
    base_datos = cliente['mascotas_db']
    coleccion_consejos = base_datos['consejos']
    consejos = list(coleccion_consejos.find({}, {'_id': 0}))
    return jsonify(consejos)

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=puerto)