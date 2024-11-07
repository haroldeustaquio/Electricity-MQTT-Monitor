# Electricity MQTT Monitor

This repository provides a solution to monitor electricity levels using the MQTT protocol. We extract the data from MQTT, store it in several JSON files and select specific information to store in a database and generate alerts using WhatsApp.

---

## Project Description

### 1. Configuration and Extraction from MQTT

#### MQTT Broker Configuration:

The connection details to the MQTT broker are specified in the `broker.json` file, which should have the following structure:

```json
{
"broker": "",
"port": "",
"topics": ""
}
```
This file defines the MQTT broker, the connection port and the subscription topics to receive the monitoring data.

---

### 2. Data Processing and Storage

#### Storage Files

- ``history.json``: Stores all the information received from MQTT to keep a complete record of the data.
- ``last_update.json``: Stores only the last update received, allowing quick access to the most recent information.
- ``part_1.json`` and ``part_2.json``: These are temporary files used to join partial messages. These files help to concatenate the data that, at the end of the process, is saved in ``history.json``.

#### Selecting IDs

[in process...]

#### Database Storage

[in process...]

---

### 3. WhatsApp Notification

[in process...]

---

## Dependencies

This project requires the following libraries:

- `json`: To handle the creation and manipulation of JSON files.
- `mqtt`: Python library for communication through the MQTT protocol.