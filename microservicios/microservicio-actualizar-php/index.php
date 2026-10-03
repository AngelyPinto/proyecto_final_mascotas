<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: PUT, POST, GET, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($uri === '/api-docs' || $uri === '/api-docs/') {
    header("Content-Type: text/html; charset=UTF-8");
    ?>
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Microservicio de Actualizacion de Mascotas</title>
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
                title: "Microservicio de Actualización de Mascotas",
                version: "1.0.0",
                description: "Microservicio en PHP para actualizar información de mascotas en la base de datos."
              },
              servers: [
                { url: "https://microservicio-actualizar-php.onrender.com", description: "Servidor de Producción" }
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
                "/actualizar": {
                  put: {
                    summary: "Actualizar datos de una mascota",
                    requestBody: {
                      required: true,
                      content: {
                        "application/json": {
                          schema: {
                            type: "object",
                            properties: {
                              id: { type: "string", example: "60d5ec49f1b2c81184a2b123" },
                              nombre: { type: "string", example: "Firulais" },
                              estado: { type: "string", example: "Encontrado" }
                            }
                          }
                        }
                      }
                    },
                    responses: {
                      "200": { description: "Mascota actualizada correctamente" }
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
    <?php
    exit();
}

header("Content-Type: application/json");
echo json_encode(["mensaje" => "Microservicio de actualización (PHP) funcionando"]);