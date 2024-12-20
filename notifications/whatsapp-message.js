const qrcode = require('qrcode-terminal');
const { Client, LocalAuth } = require('whatsapp-web.js');
const sendMessage = require('./sendMessage');
const keepAlive = require('./keepAlive');
const { get_last_alert, get_penultimate_alert } = require('./data_loader'); // Import the dinamic functions

const client = new Client({
    authStrategy: new LocalAuth({
        clientId: 'session_alerts',
    }),
});

const data = require('./number_id.json');
const number = data.number;

let lastSentAlertDateTime = null; // Variable to track the last alert sent

// Function to check if current time is within allowed hours (8:00 AM to 6:00 PM)
const isWithinAllowedHours = () => {
    const now = new Date();
    const currentHour = now.getHours();
    return currentHour >= 8 && currentHour < 18;
};

// Function to check for changes between alerts
const checkForAlertChanges = () => {
    // Validate time restriction
    if (!isWithinAllowedHours()) {
        console.log('Outside allowed hours. No messages will be sent.');
        return;
    }

    const last_alert = get_last_alert();
    const penultimate_alert = get_penultimate_alert();

    // Validate if the alerts are defined
    if (!last_alert || !penultimate_alert) {
        console.log('Cannot check for changes: alerts are undefined or invalid.');
        return;
    }

    // Compare the last alert with the penultimate
    const isDifferent =
        last_alert.power_flag !== penultimate_alert.power_flag ||
        last_alert.Va_flag !== penultimate_alert.Va_flag ||
        last_alert.Vb_flag !== penultimate_alert.Vb_flag ||
        last_alert.Vc_flag !== penultimate_alert.Vc_flag ||
        last_alert.Va_b_flag !== penultimate_alert.Va_b_flag ||
        last_alert.Vb_c_flag !== penultimate_alert.Vb_c_flag ||
        last_alert.Vc_a_flag !== penultimate_alert.Vc_a_flag 
        // last_alert.current_flag !== penultimate_alert.current_flag ||


    // Check if the alert is new and process accordingly
    if (last_alert.date_time !== lastSentAlertDateTime) {
        if (isDifferent) {
            const message = `
⚠️ Change detected ⚠️
> 🕝 Date/Time: ${last_alert.date_time}
> 💡 Power: ${last_alert.power_message || 'Normal Power'}
> ⚡ Voltage A: ${last_alert.Va_message || 'Normal Voltage'}
> ⚡ Voltage B: ${last_alert.Vb_message || 'Normal Voltage'}
> ⚡ Voltage C: ${last_alert.Vc_message || 'Normal Voltage'}
> ⚡ Voltage A-B: ${last_alert.Va_b_message || 'Normal Voltage'}
> ⚡ Voltage B-C: ${last_alert.Vb_c_message || 'Normal Voltage'}
> ⚡ Voltage C-A: ${last_alert.Vc_a_message || 'Normal Voltage'}
            `.trim();
// > 🔌 Current: ${last_alert.current_message || 'Normal Current'}
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
