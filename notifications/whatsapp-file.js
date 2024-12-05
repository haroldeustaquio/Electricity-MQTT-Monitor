const qrcode = require('qrcode-terminal');
const { Client, LocalAuth } = require('whatsapp-web.js');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const sendFile = require('./sendFile'); // Importar la función personalizada

// Configuración del cliente de WhatsApp
const client = new Client({
    authStrategy: new LocalAuth(),
});

// Número al que se enviarán las alertas o respuestas (cambia según sea necesario)
const number = '51973434110@c.us';

// Ruta del script de Python y carpeta de imágenes
const pythonScriptPath = path.join(__dirname, '../media_outputs/generate_images.py');
const imagesFolder = path.join(__dirname, '../media_outputs/images/');

// Escanea el QR para autenticarte
client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

// Evento: cuando el cliente esté listo
client.on('ready', () => {
    console.log('Client is ready!');

    // Programar alertas diarias a las 8:00, 12:00 y 18:00
    const alertTimes = ['08:00', '12:00', '18:00'];
    alertTimes.forEach((time) => {
        const [hour, minute] = time.split(':');
        schedule.scheduleJob({ hour: parseInt(hour), minute: parseInt(minute) }, () => {
            runPythonScript(() => {
                sendGeneratedImages(number);
            });
        });
    });
});

// Función para ejecutar el script de Python
function runPythonScript(callback) {
    exec(`python "${pythonScriptPath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error ejecutando el script de Python: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Error del script de Python: ${stderr}`);
        }
        console.log(`Resultado del script de Python: ${stdout}`);
        callback();
    });
}

// Función para enviar las imágenes generadas usando sendFile.js
function sendGeneratedImages(chatId) {
    fs.readdir(imagesFolder, (err, files) => {
        if (err) {
            console.error(`Error leyendo la carpeta de imágenes: ${err.message}`);
            return;
        }

        const imageFiles = files.filter(file => file.endsWith('.png')); // Filtrar solo imágenes PNG
        if (imageFiles.length === 0) {
            client.sendMessage(chatId, 'No se encontraron imágenes generadas.');
            return;
        }

        imageFiles.forEach(image => {
            const imagePath = path.join(imagesFolder, image);
            sendFile(client, chatId, imagePath, image); // Usar sendFile para enviar el archivo
        });
    });
}

// Escuchar mensajes entrantes
client.on('message', (message) => {
    if (message.body.toLowerCase() === 'imagen') {
        // Ejecutar el script de Python y luego enviar las imágenes generadas
        runPythonScript(() => {
            sendGeneratedImages(message.from);
        });
    }
});

// Inicia el cliente
client.initialize();
