# Electricity MQTT Monitor

## Overview
The **Electricity MQTT Monitor** provides an integrated solution for monitoring and notifying electrical anomalies in real time. Combining two key components, **Monitor** and **Notifications**, this repository uses the MQTT protocol to collect data, process it, and notify users via WhatsApp when significant changes are detected. It is designed for seamless performance with robust anomaly detection, real-time data tracking, and user-friendly notifications.

**Content**
- [Monitor](#monitor)
  - [Key Features](#key-features)
  - [File Structure](#file-structure)
- [Notifications](#notifications)
  - [Key Features](#key-features-1)
  - [File Structure](#file-structure-1)
- [Installation](#installation)

---

## Monitor

### Key Features
- Collects real-time electrical data (voltage, current, power) through MQTT topics.
- Processes data for anomaly detection using statistical and machine learning methods.
- Stores processed results and raw data in structured JSON files for historical analysis.
- Generates alerts for significant deviations or abnormal readings, which are used for external notifications.

### File Structure

- **`main.py`**: The main script that initializes the MQTT client, connects to the broker, and continuously listens for messages on the specified topic.
- **`functions/`**:
  - **`mqtt_extraction.py`**: Handles MQTT configuration, connects to the broker, and processes incoming messages.
  - **`file_handling.py`**: Manages JSON file operations like reading, writing, and updating.
  - **`voltage_detector.py`**: Detects anomalies in voltage data.
  - **`current_detector.py`**: Identifies irregularities in current measurements.
  - **`power_detector.py`**: Monitors power data for abnormal patterns.
- **`data/`**:
  - **`history.json`**: Logs all received MQTT data.
  - **`last_update.json`**: Stores the most recent data received for quick access.
  - **`part_1.json`** and **`part_2.json`**: Store partial data during processing.
- **`alerts/`**:
  - **`alerts.json`**: Contains the most recent alert with detailed information.
  - **`history_alerts.json`**: Maintains a historical record of all generated alerts.
- **`broker.json`**: Configuration file with MQTT broker details, including:
  - **`broker`**: The MQTT broker URL.
  - **`port`**: The port to connect to the broker.
  - **`topics`**: The MQTT topic to subscribe to.

---

## Notifications

### Key Features
- Monitors alert data in JSON files for real-time changes.
- Sends automated WhatsApp notifications for significant anomalies in electrical parameters.
- Ensures no duplicate alerts by tracking previously sent notifications.
- Maintains active WhatsApp sessions with periodic keep-alive mechanisms.

### File Structure
- **`data_loader.js`**: Loads real-time alert data from JSON files and tracks updates.
- **`whatsapp-message.js`**: Initializes the WhatsApp client, detects alert changes, and sends notifications.
- **`sendMessage.js`**: Sends text messages to the target WhatsApp number or group.
- **`sendFile.js`**: Allows sending files (e.g., logs or reports) via WhatsApp.
- **`keepAlive.js`**: Keeps the WhatsApp session active to prevent disconnections.

---

## Installation

Ensure you have **`Node.js`** for the Notifications module and **`Python`** for the Monitor module installed on your system.

### 1. **Clone the repository:**

```bash
git clone https://github.com/haroldeustaquio/Electricity-MQTT-Monitor.git
```

### 2. **Navigate to the desired module**:

* For **``monitor``**:
    ```bash
    cd monitor
    ```

* For **``notifications``**:
    ```bash
    cd notifications
    ```

### 3. **Install dependencies**:

* For **``monitor``**:
    ```bash
    pip install paho-mqtt numpy scipy statsmodels scikit-learn
    ```

* For **``notifications``**:
    ```bash
    npm install whatsapp-web.js qrcode-terminal fs
    ```


### 4. **Run the desired script**:

* For **``monitor``**:
    ```bash
    python main.py
    ```

* For **``notifications``**:
    ```bash
    node whatsapp-message.js
    ```


### 5. Scan QR code (Notifications only):

Once the notification bot starts, scan the QR code displayed in the terminal with the WhatsApp app to log in.

---

<div align="center"> 
    <em> 
        Collaboration drives innovation! If you have ideas, suggestions, or improvements, feel free to open an issue or submit a pull request. Together, we can make this project even better! 
    </em> 
</div>