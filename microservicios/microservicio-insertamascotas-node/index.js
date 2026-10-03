const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Variables de entorno de MongoDB Data API
const MONGO_DATA_API_URL = process.env.MONGO_DATA_API_URL;
const MONGO_DATA_API_KEY = process.env.MONGO_DATA_API_KEY;
const MONGO_DATA_SOURCE = process.env.MONGO_DATA_SOURCE;
const MONGO_DATABASE = process.env.MONGO_DATABASE;
const MONGO_COLLECTION = process.env.MONGO_COLLECTION;

// Ruta raíz
app.get('/', (req, res) => {
    res.json({ mensaje: "Microservicio de inserción de mascotas (Node.js) funcionando correctamente" });
});

// Redirección de la documentación Swagger a SwaggerHub
app.get('/api-docs', (req, res) => {
    res.redirect('https://app.swaggerhub.com/apis-docs/uninpahu-b8e/microservicio-insertar-node/1.0.0');
});

// Endpoint para insertar mascotas
app.post('/insertar', async (req, res) => {
    const datosMascota = req.body;

    if (!datosMascota || Object.keys(datosMascota).length === 0) {
        return res.status(400).json({ error: "Datos de mascota no válidos" });
    }

    try {
        const response = await fetch(`${MONGO_DATA_API_URL}/action/insertOne`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Request-Headers': '*',
                'api-key': MONGO_DATA_API_KEY
            },
            body: JSON.stringify({
                dataSource: MONGO_DATA_SOURCE,
                database: MONGO_DATABASE,
                collection: MONGO_COLLECTION,
                document: datosMascota
            })
        });

        const data = await response.json();

        if (data.insertedId) {
            res.status(200).json({
                mensaje: "Mascota insertada correctamente",
                id: data.insertedId
            });
        } else {
            res.status(500).json({ error: "No se pudo insertar la mascota", detalles: data });
        }
    } catch (error) {
        res.status(500).json({ error: "Error de servidor al conectar con la base de datos", detalles: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Servidor de Node.js corriendo en el puerto ${PORT}`);
});