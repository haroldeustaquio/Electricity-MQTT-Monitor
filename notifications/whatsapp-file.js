const qrcode = require('qrcode-terminal');
const { Client, LocalAuth } = require('whatsapp-web.js');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const sendFile = require('./sendFile');
const schedule = require('node-schedule');

const client = new Client({
    authStrategy: new LocalAuth({
        clientId: 'session_images',
    }),
});

const data = require('./number_id.json');
const number = data.number;


const pythonScriptPath = path.join(__dirname, '../media_outputs/image_generator.py');
const imagesFolder = path.join(__dirname, '../media_outputs/images/');

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('Client is ready!');

    // Schedule daily alerts at 8:00, 12:00 and 18:00
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

// Function to execute the Python script
function runPythonScript(callback) {
    exec(`python "${pythonScriptPath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error running Python script: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Python script error: ${stderr}`);
        }
        console.log(`Python script output: ${stdout}`);
        callback();
    });
}

// Function to send all generated images
function sendGeneratedImages(chatId) {
    fs.readdir(imagesFolder, (err, files) => {
        if (err) {
            console.error(`Error reading images folder: ${err.message}`);
            return;
        }

        const imageFiles = files.filter(file => file.endsWith('.png')); // Filter only PNG images
        if (imageFiles.length === 0) {
            client.sendMessage(chatId, 'No generated images were found.');
            return;
        }

        imageFiles.forEach(image => {
            const imagePath = path.join(imagesFolder, image);
            sendFile(client, chatId, imagePath, image); // Use sendFile to send the file
        });
    });
}

// Function to send a specific image
function sendSpecificImage(chatId, imageName) {
    const imagePath = path.join(imagesFolder, `${imageName}.png`); // Construct the specific image path

    fs.access(imagePath, fs.constants.F_OK, (err) => {
        if (err) {
            client.sendMessage(chatId, `The image '${imageName}' was not found.`);
            return;
        }

        sendFile(client, chatId, imagePath, `${imageName}.png`); // Send the specific file
    });
}

// Listen for incoming messages
client.on('message', (message) => {
    const command = message.body.toLowerCase();

    if (message.from !== number) {
        return; // Message from unauthorized chat
    }
    if (command === 'image') {
        // Run the Python script and send all images
        runPythonScript(() => {
            sendGeneratedImages(message.from); // Send all images
        });
    } else if (['image energy', 'image power', 'image voltage'].includes(command)) {
        const imageName = command.split(' ')[1]; // Extract the specific image name
        runPythonScript(() => {
            sendSpecificImage(message.from, imageName); // Send the specific image
        });
    }
});

client.initialize();
