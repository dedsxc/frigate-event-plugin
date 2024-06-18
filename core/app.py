import threading

import mqtt.mqtt_client as mqtt_client
from web.route import app

if __name__ == '__main__':
    b = mqtt_client.Broker()
    t = threading.Thread(target=b.run)
    t.start()

    a = threading.Thread(target=app.run, args=("0.0.0.0", 5000))
    a.start()

    t.join()
    a.join()
