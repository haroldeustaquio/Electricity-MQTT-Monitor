import paho.mqtt.client as mqtt
from functions import mqtt_extraction

broker, port, topic = mqtt_extraction.return_broker_data()


# Create the client MQTT
client = mqtt.Client()

client.on_connect = mqtt_extraction.on_connect
client.on_message = mqtt_extraction.on_message

client.connect(broker, port)

# Mantain the client in loop to recibe messages
client.loop_forever()