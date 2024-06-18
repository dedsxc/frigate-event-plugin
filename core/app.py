from flask import Flask, jsonify, render_template
import threading

import mqtt.mqtt_client as mqtt_client

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def get_events():
    return jsonify(mqtt_client.EVENTS)

if __name__ == '__main__':
    b = mqtt_client.Broker()
    t = threading.Thread(target=b.run)
    t.start()

    a = threading.Thread(target=app.run)
    a.start()

    t.join()
    a.join()
