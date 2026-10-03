<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: PUT, POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$data = json_decode(file_get_contents("php://input"), true);

if ($_SERVER['REQUEST_METHOD'] === 'PUT' || $_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($data['id']) && isset($data['texto'])) {
        echo json_encode([
            "status" => "success",
            "message" => "Registro actualizado correctamente",
            "data" => $data
        ]);
    } else {
        http_response_code(400);
        echo json_encode([
            "status" => "error",
            "message" => "Se requiere 'id' y 'texto'"
        ]);
    }
} else {
    echo json_encode([
        "status" => "online",
        "message" => "Microservicio de actualización PHP activo"
    ]);
}
?>