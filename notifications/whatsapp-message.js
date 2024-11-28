const qrcode = require('qrcode-terminal');
const { Client, LocalAuth } = require('whatsapp-web.js');
const sendMessage = require('./sendMessage');
const keepAlive = require('./keepAlive');
const { get_last_alert, get_penultimate_alert } = require('./data_loader'); // Import the dinamic functions

const client = new Client({
    authStrategy: new LocalAuth(),
});

const number = '51973434110@c.us'; // Test number

let lastSentAlertDateTime = null; // Variable to track the last alert sent

// Function to check for changes between alerts
const checkForAlertChanges = () => {
    const last_alert = get_last_alert();
    const penultimate_alert = get_penultimate_alert();

    // Validate if the alerts are defined
    if (!last_alert || !penultimate_alert) {
        console.log('Cannot check for changes: alerts are undefined or invalid.');
        return;
    }

    // Compare the last alert with the penultimate
    const isDifferent =
        last_alert.voltage_flag !== penultimate_alert.voltage_flag ||
        last_alert.current_flag !== penultimate_alert.current_flag ||
        last_alert.power_flag !== penultimate_alert.power_flag;

    // Check if the alert is new and process accordingly
    if (last_alert.date_time !== lastSentAlertDateTime) {
        if (isDifferent) {
            const message = `
⚠️ Change detected ⚠️
> 🕝 Date/Time: ${last_alert.date_time}
> ⚡ Voltage: ${last_alert.voltage_message || 'Normal Voltage'}
> 🔌 Current: ${last_alert.current_message || 'Normal Current'}
> 💡 Power: ${last_alert.power_message || 'Normal Power'}
            `.trim();

            console.log('Generated message:', message);
            sendMessage(client, number, message);

            // Update the last sent alert
            lastSentAlertDateTime = last_alert.date_time;
        } else {
            console.log('Alert is new but no significant changes detected.');
        }
    } else {
        console.log('Alert already sent. No action required.');
    }
};

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('Scan the QR code to log in.');
});

client.on('ready', () => {
    console.log('Client is ready!');

    keepAlive(client);

    // Check for changes every 60 seconds
    setInterval(() => {
        checkForAlertChanges();
    }, 30000);
});

// Initialize the client
client.initialize();
