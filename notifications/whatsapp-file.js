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
    const command = message.body.toLowerCase().trim(); // Convert to lowercase and trim spaces

    const validImages = ['power', 'voltage_1', 'voltage_2', 'energy'];
    const allImagesCommand = 'image'; // Command to send all images

    // Check if the message is from an authorized number
    // if (message.from !== number) {
    //     console.log('Unauthorized sender:', message.from);
    //     return; // Ignore messages from unauthorized numbers
    // }

    if (command === allImagesCommand) {
        // Send all images
        console.log('Sending all images...');
        runPythonScript(() => {
            sendGeneratedImages(message.from); // Function to send all images
        });
    } else if (command.startsWith('image')) {
        // Extract the specific image name from the command
        const imageName = command.split(' ')[1]; // Get the second word after 'image'

        if (imageName === 'voltage') {
            console.log('Sending voltage images: voltage_1 and voltage_2');
            runPythonScript(() => {
                sendSpecificImage(message.from, 'voltage_1'); // Send voltage_1
                sendSpecificImage(message.from, 'voltage_2'); // Send voltage_2
            });
        } else if (validImages.includes(imageName)) {
            console.log(`Sending specific image: ${imageName}`);
            runPythonScript(() => {
                sendSpecificImage(message.from, imageName); // Function to send the specific image
            });
        } else {
            console.log(`Invalid image name: ${imageName}`);
        }
    } else {
        console.log(`Unknown command: ${command}`);
    }
});


client.initialize();
