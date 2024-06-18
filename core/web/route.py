from flask import Flask, jsonify, render_template, request

import mqtt.mqtt_client as mqtt_client

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def get_events():
    return jsonify(mqtt_client.EVENTS)

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    data = request.get_json()
    alarm_state = data.get('alarm_state')
    if alarm_state == "on":
        mqtt_client.ALARM_ON = True
    else:
        mqtt_client.ALARM_ON = False
    print(f"[flask] Alarm state updated: ALARM_ON={mqtt_client.ALARM_ON}")
    return jsonify({"message": "Alarm state updated."})
