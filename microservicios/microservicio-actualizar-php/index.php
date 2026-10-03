<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");

if ($_SERVER['REQUEST_URI'] === '/api-docs' || $_SERVER['REQUEST_URI'] === '/api-docs/') {
    echo json_encode(["mensaje" => "Documentacion del microservicio de actualizacion (PHP)"]);
    exit();
}

echo json_encode(["mensaje" => "Microservicio de actualización (PHP) funcionando"]);