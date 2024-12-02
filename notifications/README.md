# Electricity Notifications

## Overview

The **``Electricity Notifications``** is a real-time system that monitors electrical parameters like voltage, current, and power. It integrates with WhatsApp to send automated alerts when anomalies are detected, using data from JSON files to track changes. The system ensures seamless operation with active session management and periodic monitoring, providing a simple and efficient solution for real-time notifications.


**Content**
- [Architecture](#architecture)
- [Usage](#usage)
- [Functions](#functions)
    - [data_loader](#data_loaderjs)
    - [keepAlive](#keepalivejs)
    - [sendFile](#sendfilejs)
    - [sendMessage](#sendmessagejs)
    - [whatsapp-message](#whatsapp-messagejs)
- [Installation](#installation)

---

## Architecture

<p align="center">
  <img src="https://github.com/user-attachments/assets/e543d884-fbaf-48e9-9035-fc39b3d9c7ed" alt="Architecture">
</p>


<div align="center">
    <em>Figure 1: Architecture of Electricity Notifications</em>
</div>



---

## Usage

* **Initialization:**
    - The program initializes the WhatsApp client using the `whatsapp-web.js` API and generates a QR code for authentication.
    - Once logged in, the session is maintained using the `keepAlive` module to prevent disconnections.
    - The `data_loader` module loads real-time alert data from `last_alert.json` and `history_alerts.json` located in the `monitor/alerts/` directory.

* **Alert Monitoring:**
    - The `data_loader` module tracks updates in the JSON files to fetch the latest (`last_alert`) and penultimate (`history_alerts`) alerts.
    - The `whatsapp-message.js` file compares the two alerts to detect changes in voltage, current, or power flags.

* **Automated Notifications:**
    - **Text Messages**:
        - When significant changes are detected in the alerts, a formatted message is generated with details on the voltage, current, and power statuses.
        - The `sendMessage` function sends the message to the specified WhatsApp number or group, ensuring no duplicate messages are sent by tracking the last alert sent.

    - **File Sending**:
        - The `sendFile` module allows attaching and sending files to the same target number or group if required.
        - File path and file name must be configured before sending.

    - **Continuous Execution**:
        - The program checks for changes in the alert data at regular intervals (default: 30 seconds).
        - The WhatsApp session is kept alive with periodic logs to prevent timeouts or disconnections.





## Functions

### `whatsapp-message.js`
This is the main file that initializes the WhatsApp client. It includes the following functions:

- **`qrcode`**: Generates a QR code that you need to scan with the WhatsApp app to log in.
- **`sendMessage`**: Sends a text message to the target number or group when it detects alert changes. It also prevents duplicate notifications by tracking the last alert sent.
- **`sendFile`**: Sends a file to the target number or group.
- **`keepAlive`**: Keeps the WhatsApp session active by sending periodic logs to avoid disconnections.


### `data_loader.js`
This file is responsible for loading and monitoring alert data from JSON files located in the `monitor/alerts/` directory. It includes the following functions:

- **`loadAlerts`**: Reads the `last_alert.json` file to load the most recent alert. Updates the `last_alert` variable for use in other parts of the system.
- **`loadHistoryAlerts`**: Reads the `history_alerts.json` file to load the penultimate alert. Updates the `penultimate_alert` variable if enough historical data is available.
- **`fs.watch`**: Monitors `last_alert.json` and `history_alerts.json` for changes. Triggers data reloads with a debounce mechanism to ensure timely updates without excessive processing.
- **`get_last_alert` and `get_penultimate_alert`**: Exported utility functions that provide access to the latest and penultimate alerts for external modules.

### `sendMessage.js`
This file exports a function that sends a text message to a WhatsApp number:

**Parameters**:
- **`client`**: Instance of the WhatsApp client.
- **`number`**: WhatsApp number (in `51XXXXXXXXX@c.us` format).
- **`message`**: The text of the message to send.

### `sendFile.js`
This file exports a function that sends a file to a WhatsApp number:

**Parameters**:
- **`client`**: WhatsApp client instance.
- **`number`**: WhatsApp number (in `51XXXXXXXXX@c.us` format).
- **`filePath`**: Local path of the file to be sent.
- **`fileName`**: Name of the file to display on WhatsApp.

### `keepAlive.js`
This file exports a function that keeps the WhatsApp session active:

**Function**:
- Runs a periodic function (every 5 minutes) that keeps the session alive by printing a message to the console.

---

## Installation

To run this project, make sure you have ``Node.js`` installed and follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/haroldeustaquio/Electricity-MQTT-Monitor
```

### 2. Go to ``notifications`` folder
```bash
cd notifications
```

### 3. Install dependencies:

```bash
npm install whatsapp-web.js qrcode-terminal fs
```

### 4. Run the bot

```bash
node whatsapp-message.js
```

### 5. Scan QR code

Once you run the bot, a QR code will be generated in the terminal. Scan it with the WhatsApp app to log in.

---

<div align="center">
    <em>
      We believe in the power of collaboration and the amazing things we can achieve together. If you have ideas, suggestions, or improvements, feel free to open an issue or submit a pull request. Let’s make this project even better—your contributions are always welcome!
    </em>
</div>