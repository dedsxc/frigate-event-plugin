from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

EVENTS_FILE = 'events.json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def get_events():
    events = []
    try:
        with open(EVENTS_FILE, 'r') as f:
            for line in f:
                events.append(json.loads(line.strip()))
    except FileNotFoundError:
        pass
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
