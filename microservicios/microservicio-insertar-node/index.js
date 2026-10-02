const express = require('express');
const { MongoClient } = require('mongodb');

const app = express();
app.use(express.json());

const uri = process.env.MONGO_URI;
const cliente = new MongoClient(uri);
let coleccion;

async function conectar() {
    await cliente.connect();
    const db = cliente.db('mascotas_db');
    coleccion = db.collection('consejos');
}

conectar();

app.get('/', (req, res) => {
    res.json({ mensaje: 'Microservicio de insercion de consejos (Node.js) funcionando' });
});

app.post('/insertar', async (req, res) => {
    const { texto } = req.body;

    if (!texto) {
        return res.status(400).json({ error: 'Se necesita el campo texto' });
    }

    const resultado = await coleccion.insertOne({ texto });
    res.json({ mensaje: 'Consejo insertado correctamente', id: resultado.insertedId });
});

app.get('/consejos', async (req, res) => {
    const consejos = await coleccion.find({}).toArray();
    res.json(consejos);
});

const puerto = process.env.PORT || 3000;
app.listen(puerto, () => {
    console.log('Servidor corriendo en el puerto ' + puerto);
});
