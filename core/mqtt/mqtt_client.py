import paho.mqtt.client as mqtt
import os
import json

from notification.notification import Notification

EVENTS = []
ALARM_ON = False

class Broker:
    def __init__(self):
        self.mqtt_broker = os.environ['MQTT_BROKER']
        self.mqtt_port = 1883
        self.mqtt_client_id = "python-mqtt"
        self.mqtt_topic = "frigate/events"
        self.mqtt_username = os.environ['MQTT_USER']
        self.mqtt_password = os.environ['MQTT_PASSWORD']
        self.notification = Notification(
            ssh_host=os.environ['SSH_HOST'],
            ssh_port=22,
            ssh_username=os.environ['SSH_USER'],
            ssh_password=os.environ['SSH_PASSWORD']
        )

    # Function to filter events and save
    def _process_event(self, event_json):
        # Check if event meets criteria (False_positive=false)
        if not event_json["before"]["false_positive"]:
            # Remove outdated events with the same ID
            global EVENTS
            EVENTS = [
                event for event in EVENTS
                if event["before"]["id"] != event_json["before"]["id"]
                   or event["before"]["start_time"] >= event_json["before"]["start_time"]
            ]
            # Add the new event if it wasn't found in the removal step
            if not any(event["before"]["id"] == event_json["before"]["id"] for event in EVENTS):
                EVENTS.append(event_json)
                if ALARM_ON:
                    self.notification.connect()
                    self.notification.execute_command('cd $HOME/git/sentinel-audio-alarm && ./audio.py -f attention')
                    self.notification.close()
                else:
                    print(f"[mqtt] Alarm is disabled. Send welcome message")
                    self.notification.connect()
                    self.notification.execute_command('cd $HOME/git/sentinel-audio-alarm && ./audio.py -f welcome')
                    self.notification.close()


    # MQTT callback functions
    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print(f"[mqtt] Connected to {self.mqtt_broker}:{self.mqtt_port} on topic={self.mqtt_topic}")
            client.subscribe(self.mqtt_topic)
        else:
            print(f"[mqtt] Failed to {self.mqtt_broker}:{self.mqtt_port} on topic={self.mqtt_topic}")
            exit(1)

    def _on_message(self, client, userdata, msg):
        event_data = msg.payload.decode()
        print(f"[mqtt] New event received: {event_data}")
        try:
            self.event_json = json.loads(event_data)
            self._process_event(self.event_json)
        except json.JSONDecodeError as e:
            print(f"[mqtt] Failed to decode JSON: {e}")

    def run(self):
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=self.mqtt_client_id)
        mqtt_client.username_pw_set(self.mqtt_username, self.mqtt_password)
        mqtt_client.on_connect = self._on_connect
        mqtt_client.on_message = self._on_message
        mqtt_client.connect(self.mqtt_broker, self.mqtt_port, 60)
        mqtt_client.loop_forever()
