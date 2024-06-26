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
    mqtt_client.ALARM_ON = data.get('alarm_state')
    mqtt_client.START_TIME = data.get('start_time')
    mqtt_client.END_TIME = data.get('end_time')
    print(f"[flask] Alarm state updated: ALARM_ON={mqtt_client.ALARM_ON}")
    return jsonify({"message": "Alarm state updated."})

@app.route('/alarm_state', methods=['GET'])
def get_alarm_state():
    return jsonify({
        'startTime': mqtt_client.START_TIME,
        'endTime': mqtt_client.END_TIME,
        'alarm_state': mqtt_client.ALARM_ON
    })


if __name__ == "__main__":
    m = mqtt_client.Broker()
    t1 = Thread(target=m.run)
    t1.start()
    serve(app, host="0.0.0.0", port=8080)
    t1.join()
