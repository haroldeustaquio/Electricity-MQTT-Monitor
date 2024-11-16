import json
from functions import file_handling, voltage_detector
from datetime import datetime
import math

def return_broker_data():
    keys = file_handling.read_json('broker')

    if keys is not None:
        try:
            broker = keys['broker']
            port = keys['port']
            topic = keys['topics']
        except KeyError as e:
            print(f"Error: Key {e} not found in data/broker.json")
    else:
        print("Error: Could not load data/broker.json")
    
    return broker, port, topic


def on_connect(client, userdata, flags, rc):
    
    _, _, topic = return_broker_data()
    
    connection_codes = {
        0: "Connected to MQTT broker",
        1: "Connection error: Invalid protocol",
        2: "Connection error: Invalid client id",
        3: "Connection error: Server unavailable",
        4: "Connection error: Invalid username or password",
        5: "Connection error: Unauthorized"
    }
    
    if rc == 0:
        print(connection_codes[rc])
        try:
            client.subscribe(topic)
            print("Topic subscription successful")
        except Exception as e:
            print(f"Error subscribing to topic: {e}")
    else:
        print(connection_codes.get(rc, f"Unknown Connection Error, code: {rc}"))


def save_data():
    # Load datetime
    date_time =datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    date = {
        "date":date_time
    }
    
    # Load temp files
    part_0 = file_handling.read_json('part_0')
    part_1 = file_handling.read_json('part_1')
    
    # Check that the parts are not None
    if part_0 is None or part_1 is None:
        print("Error: Couldn't load part_0 or part_1")
        return
    
    # Combine the 2 parts in 1
    total_part = [{**date,**part_0, **part_1}]
    
    file_handling.load_update(total_part,'history')
    
    file_handling.save_json(total_part,'last_update')
    
    # Voltage
    global instant_energy 
    instant_energy = round(math.sqrt(part_0['1']**2 + part_0['2']**2 + part_0['3']**2 + part_0['4']**2 + part_0['5']**2 + part_0['6']**2),3)
    
    voltage = [{
        'date': date_time,
        'Va': part_0['1'],
        'Vb': part_0['2'],
        'Vc': part_0['3'],
        'Va-b': part_0['4'],
        'Vb-c': part_0['5'],
        'Vc-a': part_0['6'],
        'instant_energy': instant_energy
    }]
    
    # current
    current = [{
        'date': date_time,
        'Ia':part_0['7'],
        'Ib': part_0['8'],
        'Ic': part_0['9']
    }]
    
    # potency
    potency = [{
        'date': date_time,
        'total-active-power': part_0['13'],
        'total-reactive-power': part_0['17'],
        'total-apparent-power': part_0['21'],
        'total-power-factor': part_0['25'],
        'frecuency': part_0['26']
    }]
    
    # Save in voltage
    file_handling.load_update(voltage,'voltage','electrical-data')
    
    # Save in current
    file_handling.load_update(current,'current','electrical-data')
    
    # Save in potency
    file_handling.load_update(potency,'potency','electrical-data')
    
    print('Saving data... 100%')


def save_alert():
    if voltage_detector.volt_outliers(instant_energy) ==1:
        voltage_alert = {"message_1":f"Voltage Alert: {instant_energy}"}
    else:
        voltage_alert = {"message_1":""}
    
    file_handling.save_json(voltage_alert,'alerts',folder=None)
    print('go')

def on_message(client, userdata, message):
    global dicc_total, temp
    
    try:
        # Try to decode the JSON message
        temp = json.loads(str(message.payload.decode()).replace("\'}", "").replace("{\'", ""))
    except json.JSONDecodeError:
        print("Error: Received message is not valid JSON")
        return

    # Verify that the structure of `temp` is as expected
    try:
        points = temp['data'][0]['point'][1:]
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error in the structure of the message: {e}")
        return

    # Check if the value 1 is in the first point of the message
    if 1 in points[0].values():
        part_0 = points
        dicc = {item['id']: item['val'] for item in part_0}
        file_handling.save_json(dicc,'part_0')
    else:
        part_1 = points
        dicc = {item['id']: item['val'] for item in part_1}        
        file_handling.save_json(dicc,'part_1')
        save_data()
        save_alert()
