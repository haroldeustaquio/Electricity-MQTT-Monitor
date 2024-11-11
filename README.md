# Electricity MQTT Monitor

This repository provides a solution to monitor electricity levels using the MQTT protocol. We extract the data from MQTT, store it in several JSON files and select specific information to store in a database and generate alerts using WhatsApp.

<hr>

**Content**
- [Project Description](#project-description)
- [MQTT Broker Configuration](#mqtt-broker-configuration)
- [Selecting Variables](#selecting-variables)
- [Proccesing Data](#processing-data)
    - [File Handling](#file_handlingpy)
    - [MQTT Extraction](#mqtt_extractionpy)
- [Storage Files](#storage-files)
- [Electrical Analysis](#electrical-analysis)
- [WhatsApp Notification](#whatsapp-notification)


<hr>


## Project Description

[In process...]


<hr>


## MQTT Broker Configuration

The connection details to the MQTT broker are specified in the `broker.json` file, which should have the following structure:

```json
{
"broker": "",
"port": "",
"topics": ""
}
```
This file defines the MQTT broker, the connection port and the subscription topics to receive the monitoring data.

<hr>
<hr>

## Selecting Variables

#### Date and Time

| Variable      | Description                        | Format               |
|---------------|------------------------------------|----------------------|
| Date and Time | Captures the date and time of data | `YYYY-MM-DD HH:MM:SS` |

<hr>

#### Voltage (ID: 1-6)

| ID  | Variable | Description                           |
|-----|----------|---------------------------------------|
| 1   | Va       | Voltage on phase A                    |
| 2   | Vb       | Voltage on phase B                    |
| 3   | Vc       | Voltage on phase C                    |
| 4   | Va-b     | Voltage between phases A and B        |
| 5   | Vb-c     | Voltage between phases B and C        |
| 6   | Vc-a     | Voltage between phases C and A        |

<hr>


#### Current (ID: 7-9)

| ID  | Variable | Description          |
|-----|----------|----------------------|
| 7   | Ia       | Current in phase A   |
| 8   | Ib       | Current in phase B   |
| 9   | Ic       | Current in phase C   |

<hr>


#### Power (ID: 13, 17, 21, 25)

| ID  | Variable               | Description                                     |
|-----|-------------------------|-------------------------------------------------|
| 13  | Total Active Power      | Energy performing useful work                   |
| 17  | Total Reactive Power    | Energy stored in inductive or capacitive elements |
| 21  | Total Apparent Power    | Combined active and reactive power              |
| 25  | Total Power Factor      | Efficiency in power use                         |

<hr>


#### Frequency (ID: 26)

| ID  | Variable   | Description             |
|-----|------------|-------------------------|
| 26  | Frequency  | System power frequency  |


<hr>
<hr>

## Processing Data

### `file_handling.py`

#### **``save_json``**
This function saves data to a JSON file in a specified folder:

+ **Parameters**:
    - **``data``**: The content to save to the JSON file.
    - **``filename``**: The name of the JSON file (without extension).
    - **``folder``**: The folder where the JSON file will be saved (default is "data").


#### **``read_json``**
This function reads data from a specified JSON file:

+ Parameters:
    - **``filename``**: The name of the JSON file (without extension).
    - **``folder``**: The folder where the JSON file is located (default is "data").

#### **``load_update``**
This function reads an existing JSON file, appends new data if it contains a list, and saves the updated list:

+ Parameters:
    - **``data_json``**: The new data to append to the existing list in the JSON file.
    - **``filename``**: The name of the JSON file (without extension).
    - **``folder``**: The folder where the JSON file is located (default is "data").

<hr>

### `mqtt_extraction.py`

#### **``return_broker_data``**
This function retrieves broker configuration data from a JSON file.


#### **``on_connect``**

This function handles the MQTT client's connection to the broker, printing connection status messages and attempting to subscribe to a topic.

+ **Parameters**:
    - **``client``**: The MQTT client instance.
    - **``userdata``**: User-specific data passed to the callback.
    - **``flags``**: MQTT connection flags.
    - **``rc``**: Connection result code.


#### **``on_message``**

This function processes incoming MQTT messages, decodes JSON data, verifies the message structure, and saves parts of the message to a JSON file.

+ **Parameters**:
    - **``client``**: The MQTT client instance.
    - **``userdata``**: User-specific data passed to the callback.
    - **``message``**: The incoming MQTT message object.


#### **``save_data``**

This function combines and processes data from temporary JSON files, adds a timestamp, and updates separate JSON files for voltage, current, and potency.


<hr>
<hr>


## Storage Files

### **``data/``**:
- **``history.json``**: Stores all the information received from MQTT to keep a complete record of the data.
- **``last_update.json``**: Stores only the last update received, allowing quick access to the most recent information.
- **``part_1.json``** and **``part_2.json``**: These are temporary files used to join partial messages. These files help to concatenate the data that, at the end of the process, is saved in ``history.json``.

<hr>

### **``electrical-data/``**:
- **`current.json`**: Contains data on the current in each phase, used to monitor load and detect overloads.
- **`potency.json`**: Includes total active, reactive, and apparent power data, as well as power factor and frequency, to evaluate system efficiency and stability.
- **`voltage.json`**: Stores voltage measurements across phases, essential for assessing voltage stability and detecting imbalances.

<hr>
<hr>

## Electrical Analysis

[in process...]

<hr>

## WhatsApp Notification

[in process...]

<hr>

## Dependencies

This project requires the following libraries:

- `json`: To handle the creation and manipulation of JSON files.
- `mqtt`: Python library for communication through the MQTT protocol.