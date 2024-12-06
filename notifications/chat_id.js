const qrcode = require('qrcode-terminal');
const { Client, LocalAuth } = require('whatsapp-web.js');

// Client configuration
const client = new Client({
    authStrategy: new LocalAuth(),
});

// Scan the QR code to log in
client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

// Event: when the client is ready
client.on('ready', async () => {
    console.log('Client is ready.');

    // Get all chats
    const chats = await client.getChats();

    // Debug the complete list of chats
    console.log('All chats:', chats.map(chat => ({
        name: chat.name,
        id: chat.id._serialized,
        isGroup: chat.isGroup,
    })));

    // Filter only groups
    const groups = chats.filter(chat => chat.isGroup);

    if (groups.length === 0) {
        console.log('No groups found. Make sure you are part of at least one group.');
        return;
    }

    console.log('Groups found:');
    groups.forEach(group => {
        console.log(`Group name: ${group.name}`);
        console.log(`Group ID: ${group.id._serialized}`);
    });
});

// Error handling
client.on('auth_failure', () => {
    console.error('Authentication failed. Please restart the session.');
});

client.on('disconnected', (reason) => {
    console.log('Client disconnected:', reason);
});

// Start the client
client.initialize();
