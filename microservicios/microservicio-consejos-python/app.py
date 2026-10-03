import os
from flask import Flask, jsonify, render_template_string
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
cliente = MongoClient(MONGO_URI) if MONGO_URI else None

HTML_SWAGGER = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Microservicio de Consejos</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = () => {
      SwaggerUIBundle({
        dom_id: '#swagger-ui',
        spec: {
          openapi: "3.0.0",
          info: {
            title: "Microservicio de Consejos para Mascotas",
            version: "1.0.0",
            description: "Microservicio en Python para obtener recomendaciones sobre mascotas perdidas."
          },
          servers: [
            { url: "https://microservicio-consejos.onrender.com", description: "Servidor de Producción" }
          ],
          paths: {
            "/": {
              get: {
                summary: "Verificar estado del microservicio",
                responses: {
                  "200": { description: "Servicio funcionando correctamente" }
                }
              }
            },
            "/consejos": {
              get: {
                summary: "Obtener lista de consejos",
                responses: {
                  "200": { description: "Lista obtenida correctamente" }
                }
              }
            }
          }
        }
      });
    };
  </script>
</body>
</html>
"""

@app.route('/')
def inicio():
    return jsonify({'mensaje': 'Microservicio de consejos para mascotas perdidas funcionando'})

@app.route('/api-docs')
def api_docs():
    return render_template_string(HTML_SWAGGER)

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