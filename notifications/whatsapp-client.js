const fs = require('fs');
const qrcode = require('qrcode-terminal');
const { Client, LocalAuth } = require('whatsapp-web.js');
const sendMessage = require('./sendMessage');
const sendFile = require('./sendFile');
const keepAlive = require('./keepAlive');

// Ruta relativa al archivo JSON
const data = require('../monitor/alerts.json');

const client = new Client({
    authStrategy: new LocalAuth()
});

const number = '51973434110@c.us'; // Hacer prueba con num, luego pasar a grupo


const message = data['message_1'];
// const filePath = './prueba.txt'; // Cambiar ubicación del archivo
// const fileName = ''; // Nombre del archivo

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('Scan the QR code to log in.');
});


client.on('ready', () => {
    console.log('Client is ready!');

    // Enviar el mensaje inmediatamente
    sendMessage(client, number, message);
});


// Inicializar el cliente
client.initialize();
