<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: PUT, POST, GET, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// Redirección directa a SwaggerHub
if ($uri === '/api-docs' || $uri === '/api-docs/') {
    header("Location: https://app.swaggerhub.com/apis-docs/uninpahu-b8e/microservicio-actualizar-php/1.0.0", true, 302);
    exit();
}

header("Content-Type: application/json");
echo json_encode(["mensaje" => "Microservicio de actualización (PHP) funcionando"]);