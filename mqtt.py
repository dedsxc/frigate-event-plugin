import paho.mqtt.client as mqtt
import os
import json

EVENTS_FILE = 'events.json'

MQTT_BROKER = os.environ['MQTT_BROKER']
MQTT_CLIENT_ID = "python-mqtt"
MQTT_TOPIC = "frigate/events"
MQTT_USERNAME = os.environ['MQTT_USER']
MQTT_PASSWORD = os.environ['MQTT_PASSWORD']


# Function to filter events and save to file
def process_event(event_json):
    # Check if event meets criteria (False_positive=false)
    if event_json.get('before', {}).get('false_positive', False) == False:
        # Check if event ID already exists in file, update if necessary
        with open(EVENTS_FILE, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            found = False
            for line in lines:
                stored_event = json.loads(line.strip())
                if stored_event['before']['id'] == event_json['before']['id']:
                    found = True
                    if event_json['before']['start_time'] > stored_event['before']['start_time']:
                        f.write(json.dumps(event_json) + '\n')
                    else:
                        f.write(line)
                else:
                    f.write(line)
            if not found:
                f.write(json.dumps(event_json) + '\n')
            f.truncate()


# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    event_data = msg.payload.decode()
    print(f"New event received: {event_data}")
    try:
        event_json = json.loads(event_data)
        process_event(event_json)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")


# MQTT Client Setup
mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID)
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.loop_forever()
