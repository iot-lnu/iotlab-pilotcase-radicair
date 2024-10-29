import os
import json
from flask import Flask, render_template, request
from flask_mqtt import Mqtt
from settings import (MQTT_BROKER, MQTT_PORT, MQTT_USERNAME,
                      MQTT_PASSWORD)

MQTT_THRESHOLD_TOPIC = 'config/threshold' # Replace this with the actual topic
MQTT_DATA_TOPIC = 'config/data' # Replace this with the actual topic

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = MQTT_BROKER
app.config['MQTT_BROKER_PORT'] = MQTT_PORT
app.config['MQTT_USERNAME'] = MQTT_USERNAME
app.config['MQTT_PASSWORD'] = MQTT_PASSWORD
app.config['MQTT_KEEPALIVE'] = 60 

mqtt = Mqtt(app)

# Global state
state = {
    'threshold': 0,
    'temperature': 0,
    'radon': 0,
    'userId': 0,
    'secretKey': 0,
    'deviceId': 0
}

# File path for the state JSON file
STATE_FILE = '../state.json'

def load_state():
    global state 
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)

def save_state():
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def publish():
    print('Received a POST request')
    
    if request.content_type == 'application/json':
        data = request.json
        print('JSON data:', data)
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
        print('Form data:', data)
    else:
        print('Unsupported Content-Type:', request.content_type)
        return 'Unsupported Content-Type', 400
    
    state['threshold'] = data.get('threshold', 0)
    state['temperature'] = data.get('temperature', 0)
    state['radon'] = data.get('radon', 0)
    state['userId'] = data.get('userId', 0)
    state['secretKey'] = data.get('secretKey', 0)
    state['deviceId'] = data.get('deviceId', 0)

    print(f'Threshold: {state['threshold']}')
    print(f'Temperature: {state['temperature']}')
    print(f'Radon: {state['radon']}')
    print(f'User ID: {state['userId']}')
    print(f'Secret Key: {state['secretKey']}')
    print(f'Device ID: {state['deviceId']}')

    # Save the state to the JSON file
    save_state()

    json_data = {
        'temperature': state['temperature'],
        'radon': state['radon']
    }
    
    mqtt.publish(MQTT_THRESHOLD_TOPIC, state['threshold'])
    mqtt.publish(MQTT_DATA_TOPIC, json.dumps(json_data))

    return 'POST request received and data published to MQTT', 200

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(f'Received message on topic {message.topic}: {message.payload.decode()}')

@app.route('/get_state')
def get_state():
    return state

if __name__ == '__main__':
    load_state()
    app.run(port=5050, debug=True)