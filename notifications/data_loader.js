const fs = require('fs');
const path = require('path');

// Paths to the JSON files
const alerts_path = path.join(__dirname, '../monitor/alerts/last_alert.json');
const history_alerts_path = path.join(__dirname, '../monitor/alerts/history_alerts.json');

// Variables to store results
let last_alert = null;
let penultimate_alert = null;

// Variables to handle debounce
let alertsTimeout = null;
let historyAlertsTimeout = null;

// Function to load the latest alert from the alerts.json file
const loadAlerts = () => {
    fs.readFile(alerts_path, 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading the JSON file (alerts):', err);
            return;
        }
        try {
            const jsonData = JSON.parse(data);
            last_alert = jsonData;
            // console.log('Alerts data updated in last_alert');
            console.log('Alerts data updated in last_alert:', last_alert);
        } catch (parseError) {
            console.error('Error parsing the JSON file (alerts):', parseError);
        }
    });
};

// Function to load the second-to-last alert from history_alerts.json
const loadHistoryAlerts = () => {
    fs.readFile(history_alerts_path, 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading the JSON file (history_alerts):', err);
            return;
        }
        try {
            const historyAlerts = JSON.parse(data);

            // Validate if historyAlerts is a valid array
            if (Array.isArray(historyAlerts) && historyAlerts.length >= 2) {
                penultimate_alert = historyAlerts[historyAlerts.length - 2]; // Second-to-last alert
                // console.log('history_alerts data updated in penultimate_alert');
                console.log('History_alerts data updated in penultimate_alert:', penultimate_alert);
            } else {
                console.log('Not enough elements in history_alerts to retrieve the second-to-last alert.');
                penultimate_alert = null;
            }
        } catch (parseError) {
            console.error('Error parsing the JSON file (history_alerts):', parseError);
        }
    });
};

// Initial load of alerts
loadAlerts();
loadHistoryAlerts();

// Watch for changes in alerts.json
fs.watch(alerts_path, (eventType) => {
    if (eventType === 'change') {
        clearTimeout(alertsTimeout); // Cancel previous timeout
        alertsTimeout = setTimeout(() => {
            console.log('alerts.json file modified. Reloading data...');
            loadAlerts();
        }, 100); // 100ms debounce
    }
});

// Watch for changes in history_alerts.json
fs.watch(history_alerts_path, (eventType) => {
    if (eventType === 'change') {
        clearTimeout(historyAlertsTimeout); // Cancel previous timeout
        historyAlertsTimeout = setTimeout(() => {
            console.log('history_alerts.json file modified. Reloading data...');
            loadHistoryAlerts();
        }, 100); // 100ms debounce
    }
});

// Export functions for use in other files
module.exports = {
    get_last_alert: () => last_alert,
    get_penultimate_alert: () => penultimate_alert,
};
