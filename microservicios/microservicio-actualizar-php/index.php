<?php

if ($_SERVER['REQUEST_URI'] === '/api-docs') {
    header("Location: https://microservicio-actualizar-php.onrender.com/");
    exit();
}

header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: PUT, POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

echo json_encode(["mensaje" => "Microservicio de actualización (PHP) funcionando"]);