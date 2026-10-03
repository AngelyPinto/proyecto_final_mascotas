const express = require('express');
const { MongoClient } = require('mongodb');

const app = express();
app.use(express.json());

app.get('/docs', (req, res) => {
    res.sendFile(__dirname + '/docs.html');
});

app.get('/openapi.json', (req, res) => {
    res.sendFile(__dirname + '/openapi.json');
});

const uri = process.env.MONGO_URI;
const cliente = new MongoClient(uri);
let coleccion;

async function conectar() {
    await cliente.connect();
    const db = cliente.db('mascotas_db');
    coleccion = db.collection('mascotas');
}

conectar();

app.get('/', (req, res) => {
    res.json({ mensaje: 'Microservicio de insercion de mascotas (Node.js) funcionando' });
});

app.post('/insertar', async (req, res) => {
    const datosMascota = req.body;

    if (!datosMascota || Object.keys(datosMascota).length === 0) {
        return res.status(400).json({ error: 'Se requieren los datos de la mascota' });
    }

    const resultado = await coleccion.insertOne(datosMascota);
    res.json({ mensaje: 'Mascota insertada correctamente', id: resultado.insertedId });
});

const puerto = process.env.PORT || 3000;
app.listen(puerto, () => {
    console.log('Servidor corriendo en el puerto ' + puerto);
});