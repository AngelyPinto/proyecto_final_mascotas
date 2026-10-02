<?php

header('Content-Type: application/json');

$dataApiUrl = getenv('MONGO_DATA_API_URL');
$dataApiKey = getenv('MONGO_DATA_API_KEY');
$dataSource = getenv('MONGO_DATA_SOURCE');
$database = getenv('MONGO_DATABASE');
$collection = getenv('MONGO_COLLECTION');

function llamarDataApi($accion, $dataApiUrl, $dataApiKey, $body) {
    $ch = curl_init($dataApiUrl . '/action/' . $accion);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Access-Control-Request-Headers: *',
        'api-key: ' . $dataApiKey,
    ]);
    $respuesta = curl_exec($ch);
    curl_close($ch);
    return json_decode($respuesta, true);
}

$metodo = $_SERVER['REQUEST_METHOD'];
$ruta = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($ruta === '/' && $metodo === 'GET') {
    echo json_encode(['mensaje' => 'Microservicio de actualizacion de consejos (PHP) funcionando']);
    exit;
}

if ($ruta === '/actualizar' && $metodo === 'PUT') {
    $entrada = json_decode(file_get_contents('php://input'), true);

    if (!isset($entrada['id']) || !isset($entrada['texto'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Se necesita id y texto']);
        exit;
    }

    $body = [
        'dataSource' => $dataSource,
        'database' => $database,
        'collection' => $collection,
        'filter' => ['_id' => ['$oid' => $entrada['id']]],
        'update' => ['$set' => ['texto' => $entrada['texto']]],
    ];

    $resultado = llamarDataApi('updateOne', $dataApiUrl, $dataApiKey, $body);

    if (isset($resultado['matchedCount']) && $resultado['matchedCount'] > 0) {
        echo json_encode(['mensaje' => 'Consejo actualizado correctamente']);
    } else {
        http_response_code(404);
        echo json_encode(['error' => 'No se encontro un consejo con ese id']);
    }
    exit;
}

http_response_code(404);
echo json_encode(['error' => 'Ruta no encontrada']);
