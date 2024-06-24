from threading import Thread
from waitress import serve
from flask import Flask, jsonify, render_template, request
import mqtt.mqtt_client as mqtt_client

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({'status': 'OK', 'message': 'Application is running'}), 200


@app.route('/events', methods=['GET'])
def get_events():
    return jsonify(mqtt_client.EVENTS)


@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    data = request.get_json()
    alarm_state = data.get('alarm_state')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    if alarm_state == "on":
        mqtt_client.ALARM_ON = True
        mqtt_client.START_TIME = start_time
        mqtt_client.END_TIME = end_time
    else:
        mqtt_client.ALARM_ON = False
    print(f"[flask] Alarm state updated: ALARM_ON={mqtt_client.ALARM_ON}")
    return jsonify({"message": "Alarm state updated."})


if __name__ == "__main__":
    m = mqtt_client.Broker()
    t1 = Thread(target=m.run)
    t1.start()
    serve(app, host="0.0.0.0", port=8080)
    t1.join()
