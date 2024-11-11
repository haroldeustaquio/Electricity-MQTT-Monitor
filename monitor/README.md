# Monitor


## Overview

[In process...]


**Content**
- [MQTT Broker Configuration](#mqtt-broker-configuration)
- [Functions](#functions)
    - [file_handling.py](#file_handlingpy)
    - [mqtt_extraction.py](#mqtt_extractionpy)
- [Selecting Variables](#selecting-variables)
- [Storage Files](#storage-files)
- [Electrical Analysis](#electrical-analysis)
    - [Voltage](#voltage-1)

---

## Project Structure

### MQTT Broker Configuration

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

### Functions

#### `file_handling.py`

- **``save_json``**: This function saves data to a JSON file in a specified folder:

- **``read_json``**: This function reads data from a specified JSON file:

- **``load_update``**: This function reads an existing JSON file, appends new data if it contains a list, and saves the updated list:


#### `mqtt_extraction.py`

- **``return_broker_data``**: This function retrieves broker configuration data from a JSON file.

- **``on_connect``**: This function handles the MQTT client's connection to the broker, printing connection status messages and attempting to subscribe to a topic.

- **``on_message``**: This function processes incoming MQTT messages, decodes JSON data, verifies the message structure, and saves parts of the message to a JSON file.

- **``save_data``**: This function combines and processes data from temporary JSON files, adds a timestamp, and updates separate JSON files for voltage, current, and potency.

---

### Selecting Variables
<div style="display: flex;">

<div style="flex: 1; padding-right: 0px;">

#### Date and Time

| Variable      | Description                        | Format               |
|---------------|------------------------------------|----------------------|
| Date and Time | Captures the datetime| `YYYY-MM-DD HH:MM:SS` |

#### Voltage

| ID  | Variable | Description                           |
|-----|----------|---------------------------------------|
| 1   | Va       | Voltage on phase A                    |
| 2   | Vb       | Voltage on phase B                    |
| 3   | Vc       | Voltage on phase C                    |
| 4   | Va-b     | Voltage between phases A and B        |
| 5   | Vb-c     | Voltage between phases B and C        |
| 6   | Vc-a     | Voltage between phases C and A        |


#### Current

| ID  | Variable | Description          |
|-----|----------|----------------------|
| 7   | Ia       | Current in phase A   |
| 8   | Ib       | Current in phase B   |
| 9   | Ic       | Current in phase C   |

</div>

<div style="flex: 1; padding-left: 0px;">

#### Frequency

| ID  | Variable   | Description             |
|-----|------------|-------------------------|
| 26  | Frequency  | System power frequency  |

#### Power

| ID  | Variable               | Description                                     |
|-----|-------------------------|-------------------------------------------------|
| 13  | Total Active Power      | Energy performing useful work                   |
| 17  | Total Reactive Power    | Energy stored in inductive or capacitive elements |
| 21  | Total Apparent Power    | Combined active and reactive power              |
| 25  | Total Power Factor      | Efficiency in power use                         |




</div>
</div>


---

### Storage Files

#### **``data/``**:
- **``history.json``**: Stores all the information received from MQTT to keep a complete record of the data.
- **``last_update.json``**: Stores only the last update received, allowing quick access to the most recent information.
- **``part_1.json``** and **``part_2.json``**: These are temporary files used to join partial messages. These files help to concatenate the data that, at the end of the process, is saved in ``history.json``.


#### **``electrical-data/``**:
- **`current.json`**: Contains data on the current in each phase, used to monitor load and detect overloads.
- **`potency.json`**: Includes total active, reactive, and apparent power data, as well as power factor and frequency, to evaluate system efficiency and stability.
- **`voltage.json`**: Stores voltage measurements across phases, essential for assessing voltage stability and detecting imbalances.

---

### Electrical Analysis

#### Voltage

**Instantaneous energy** in electrical systems represents the total magnitude of voltage or current at a specific moment. It combines all contributions from different voltage or current sources into a single metric, offering a unified view of the total energy flowing in the system.

This measure is typically calculated using the **Euclidean norm** (or quadratic magnitude) of individual voltage or current measurements. The general formula for instantaneous energy with multiple voltages is:

$$
\text{Instantaneous Energy} = \sqrt{\sum_{i=1}^{n} V_i^2}
$$

where $V_i$ represents each voltage measurement (e.g., `Voltage A`, `Voltage B`, `Voltage C`, `Voltage AB`, `Voltage BC`, `Voltage CA`). This calculation provides a single metric that includes all voltage contributions in the system.

**Benefits of Using Instantaneous Energy for Anomaly Detection**

* Captures Total Voltage Magnitude
* Preserves the Distinct Nature of Voltages
* Detects Global System Changes
* Enhances Sensitivity to Peaks


**Implementation**



---

#### Current


**Implementation**

---

#### Power 

**Implementation**

