# Electricity Monitor


## Overview

The **``Electricity Monitor``** is a real-time system that collects, processes, and analyzes electrical data (voltage, current, power) using MQTT. It detects anomalies through statistical and machine learning methods and generates alerts for abnormal readings. The system ensures data storage for historical analysis and provides insights into system performance and stability, making it ideal for proactive electrical monitoring and management.


**Content**
- [Architecture](#architecture)
- [Usage](#usage)
- [Selecting Variables](#selecting-variables)
- [Functions](#functions)
    - [file_handling.py](#file_handlingpy)
    - [mqtt_extraction.py](#mqtt_extractionpy)
    - [Alert Detector](#alert-detector)
    - [Storage Files](#storage-files)
- [Electrical Analysis](#electrical-analysis)
    - [Voltage](#voltage-1)
    - [Current](#current-1)
    - [Power](#power-1)
- [Installation](#installation)

---

## Architecture


<p align="center">
  <img src="https://github.com/user-attachments/assets/a9a01b43-82cf-40d8-bd1f-ce0c73265e91" alt="Architecture">
</p>


<div align="center">
    <em>Figure 1: Architecture of Electricity Monitor</em>
</div>



---

## Usage

* **Initialization**
- The system initializes by configuring an MQTT client, using `broker.json` for the broker, port, and topic settings.
- Received data from MQTT topics is parsed and temporarily stored in JSON files (`part_0.json` and `part_1.json`) for processing.

* **Purpose**
- The project is designed to:
  1. **Access** real-time electrical data (e.g., voltage, current, power) through MQTT topics.
  2. **Process** this data to detect anomalies using statistical and machine learning methods.
  3. **Store** both processed results and raw data for historical analysis.
  4. **Generate Alerts** for significant deviations or abnormal readings, preparing the information for external notifications.

> [!NOTE]
> - ``MQTT Configuration``: Ensure broker details are set correctly in `broker.json`.
  ```json
  {
  "broker": "",
  "port": "",
  "topics": ""
  }
```

## Selecting Variables
<div style="display: flex;">

<div style="flex: 1; padding-right: 0px;">

### Date and Time

| Variable      | Description                        | Format               |
|---------------|------------------------------------|----------------------|
| Date and Time | Captures the datetime| `YYYY-MM-DD HH:MM:SS` |

### Voltage

| ID  | Variable | Description                           |
|-----|----------|---------------------------------------|
| 1   | Va       | Voltage on phase A                    |
| 2   | Vb       | Voltage on phase B                    |
| 3   | Vc       | Voltage on phase C                    |
| 4   | Va-b     | Voltage between phases A and B        |
| 5   | Vb-c     | Voltage between phases B and C        |
| 6   | Vc-a     | Voltage between phases C and A        |


### Current

| ID  | Variable | Description          |
|-----|----------|----------------------|
| 7   | Ia       | Current in phase A   |
| 8   | Ib       | Current in phase B   |
| 9   | Ic       | Current in phase C   |

</div>

<div style="flex: 1; padding-left: 0px;">

### Frequency

| ID  | Variable   | Description             |
|-----|------------|-------------------------|
| 26  | Frequency  | System power frequency  |

### Power

| ID  | Variable               | Description                                     |
|-----|-------------------------|-------------------------------------------------|
| 13  | Total Active Power      | Energy performing useful work                   |
| 17  | Total Reactive Power    | Energy stored in inductive or capacitive elements |
| 21  | Total Apparent Power    | Combined active and reactive power              |
| 25  | Total Power Factor      | Efficiency in power use                         |

</div>
</div>

---

## Functions

### `file_handling.py`

- **`save_json`**
  Saves data to a specified JSON file within a given folder. If the folder does not exist, it creates the folder before saving.

- **`read_json`**
  Reads and returns data from a specified JSON file. Handles exceptions if the file does not exist or contains invalid data.

- **`load_update`**
  Reads an existing JSON file, appends new data to it if the data is in a list format, and saves the updated list back to the file. Ensures data integrity by creating the file if it does not exist.



### `mqtt_extraction.py`

- **`return_broker_data`**
  Retrieves broker configuration details (broker, port, topics) from a JSON file (`broker.json`). Ensures connectivity settings are accessible for the MQTT client.

- **`on_connect`**
  Handles the MQTT client’s connection to the broker. Prints connection status messages and subscribes to the topics specified in the broker configuration.

- **`on_message`**
  Processes incoming MQTT messages:
  1. Decodes the JSON payload.
  2. Validates the structure of the incoming message.
  3. Splits and saves parts of the message into temporary JSON files (`part_0.json`, `part_1.json`) for further processing.

- **`save_data`**
  Combines and processes data from the temporary JSON files. Adds a timestamp and updates dedicated JSON files for **voltage**, **current**, and **power**.


### Alert Detector

#### **`voltage_detector.py`**

- Detects anomalies in voltage data using statistical methods (IQR, Z-Score) and machine learning techniques (ARIMA, Isolation Forest).
- An alert is triggered when:
  - At least two methods detect an anomaly.
  - The current voltage value deviates from the range defined by the last two readings (concordance check).



#### **`current_detector.py`**

- Monitors RMS current data for anomalies using IQR, ARIMA, and Isolation Forest.

- An alert is generated when:
  - At least two detection methods indicate an anomaly.
  - The current RMS value falls outside the range of the last two readings.



#### **`power_detector.py`**

- Identifies anomalies in active power data using IQR, Z-Score, ARIMA, and Isolation Forest.

- An alert is raised when:
  - Two or more methods flag an anomaly.
  - The current power value deviates from the range defined by the last two readings.





### Storage Files

#### **``data/``**
- **``history.json``**: Stores all the information received from MQTT to keep a complete record of the data.
- **``last_update.json``**: Stores only the last update received, allowing quick access to the most recent information.
- **``part_1.json``** and **``part_2.json``**: These are temporary files used to join partial messages. These files help to concatenate the data that, at the end of the process, is saved in **``history.json``**.


#### **``electrical-data/``**
- **`current.json`**: Contains data on the current in each phase, used to monitor load and detect overloads.
- **`potency.json`**: Includes total active, reactive, and apparent power data, as well as power factor and frequency, to evaluate system efficiency and stability.
- **`voltage.json`**: Stores voltage measurements across phases, essential for assessing voltage stability and detecting imbalances.


#### **`alerts/`**
- **`alerts.json`**:  Contains the latest generated alert, including details about voltage, current, and power anomalies. This file is updated whenever a new alert is triggered.
- **`history_alerts.json`**:  Maintains a historical record of all alerts generated over time. 

This files serves as a reference for tracking past anomalies and is also used as the source for sending external notifications (e.g., via WhatsApp).

---


## Electrical Analysis

### Voltage

**Instantaneous energy** in electrical systems represents the total magnitude of voltage or current at a specific moment. It combines all contributions from different voltage or current sources into a single metric, offering a unified view of the total energy flowing in the system.

This measure is typically calculated using the **Euclidean norm** (or quadratic magnitude) of individual voltage or current measurements. The general formula for instantaneous energy with multiple voltages is:

$$\text{Instantaneous Energy} = \sqrt{\sum_{i=1}^{n} V_i^2}$$


where $V_i$ represents each voltage measurement (e.g., **`Voltage A`**, **`Voltage B`**, **`Voltage C`**, **`Voltage AB`**, **`Voltage BC`**, **`Voltage CA`**). This calculation provides a single metric that includes all voltage contributions in the system.

**Benefits of Using Instantaneous Energy for Anomaly Detection**
  * Captures Total Voltage Magnitude
  * Preserves the Distinct Nature of Voltages
  * Detects Global System Changes
  * Enhances Sensitivity to Peaks

### Current

**Root Mean Square (RMS) Current** is a key metric in electrical systems used to represent the effective value of an alternating current (AC) or varying current. It provides a single value that corresponds to the equivalent direct current (DC) value delivering the same power to a resistive load. The RMS value is particularly useful for assessing the magnitude of current over time in complex systems.

The **RMS Current** is calculated using the **quadratic mean** of individual current measurements. This method ensures that both positive and negative variations of the current contribute meaningfully to the overall value. The general formula for RMS Current is:

$$
\text{RMS Current} = \sqrt{\frac{\sum_{i=1}^{n} I_i^2}{n}}
$$

where $I_i$ represents each current measurement (e.g., **`Current A`**, **`Current B`**, **`Current C`**).

**Benefits of Using RMS Current for Monitoring and Analysis**
* Represents Effective Current Magnitude
* Smooths Out Variations in Current
* Sensitive to Fluctuations


### Power 

**Power** is a fundamental measure in electrical systems, representing the rate at which energy is transferred or converted. Power can be categorized into three key types: active power (real power), reactive power, and apparent power. These metrics are essential for analyzing and monitoring the performance and efficiency of electrical systems.

In this implementation, **active power** is directly extracted from a single variable, making the computation straightforward and efficient. Alongside active power, other key parameters such as reactive power, apparent power, power factor, and frequency are also tracked for a comprehensive understanding of the system.


**Benefits of Using Active Power for Monitoring and Analysis**
* Direct Evaluation of Energy Delivered to Loads
* Precise Monitoring of System Demand in Real-Time
* Detection of Overloads and Inefficient Operation

---

## Installation


### 1. Clone the repository

```bash
git clone https://github.com/haroldeustaquio/Electricity-MQTT-Monitor
```

### 2. Go to ``monitor`` folder
```bash
cd monitor
```

### 3. Install dependencies:

```bash
pip install paho-mqtt numpy scipy statsmodels scikit-learn
```

### 4. Run the main script

```bash
python main.py
```

### 5. Alerts and Data Monitoring

The project monitors real-time electrical data (``voltage``, ``current``, ``power``) and generates alerts for anomalies. Alerts are saved in **``alerts/``** json and historical data is logged for further analysis.

---

<div align="center">
    <em>
      We believe in the power of collaboration and the amazing things we can achieve together. If you have ideas, suggestions, or improvements, feel free to open an issue or submit a pull request. Let’s make this project even better—your contributions are always welcome!
    </em>
</div>