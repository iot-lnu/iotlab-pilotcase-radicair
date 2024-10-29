import requests
import time
import threading
import json
import logging
from dotenv import load_dotenv

class SensorDataGetter:

    def __init__(self, data_sender, request_interval=60):
        load_dotenv()
        self.data_sender = data_sender
        self.user_id = ''
        self.secret_key = ''
        self.device_id = ''

        self.TIME_TO_SLEEP = 5
        self._request_interval = request_interval
        self.lock = threading.Lock()
        self.data = {
            'time': 0,
            'battery': 0,
            'co2': 0,
            'humidity': 0,
            'pm1': 0,
            'pm25': 0,
            'pressure': 0,
            'radonShortTermAvg': 0,
            'relayDeviceType': '',
            'temp': 0,
            'voc': 0
        }
        self._stop_event = threading.Event()

    def start(self):
        
        def worker():
            while not self._stop_event.is_set():
                try:
                    with open('state.json', 'r') as file:
                        state = json.load(file)
                        self.user_id = state.get('userId')
                        self.secret_key = state.get('secretKey')
                        self.device_id = state.get('deviceId')
                        
                        # Check if all three values are set
                        if self.user_id and self.secret_key and self.device_id:
                            break
                        else:
                            print("Values not set yet. Sleeping for", self.TIME_TO_SLEEP, "seconds.")
                            time.sleep(self.TIME_TO_SLEEP)
                except Exception as e:
                    logging.warning(f'Error reding state file in sensordatagetter {e}')
                    time.sleep(self.TIME_TO_SLEEP)

            while True:
                self._request_data()
                time.sleep(self._request_interval)

        self.thread = threading.Thread(target=worker)
        self.thread.start()

    def stop(self):
        self._stop_event.set()
        self.thread.join()

    def print_data_from_key(self, key):
        with self.lock:
            print(f"{key.capitalize()}: {self.data[key]}")
            print()

    def print_data(self, key=''):
        with self.lock:
            for key, value in self.data.items():
                print(f"{key.capitalize()}: {value}")
            print()

    def get_latest_data(self):
        with self.lock:
            return self.data.copy()

    def _request_data(self):
        try:
            token_url = 'https://accounts-api.airthings.com/v1/token'
            token_data = {
                'grant_type': 'client_credentials',
                'client_id': self.user_id,
                'client_secret': self.secret_key
            }

            response = requests.post(token_url, json=token_data)
            response.raise_for_status()
            token_info = response.json()
            access_token = token_info['access_token']

            data_url = f'https://ext-api.airthings.com/v1/devices/{self.device_id}/latest-samples'
            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            response = requests.get(data_url, headers=headers)
            response.raise_for_status()
            sensor_data = response.json()['data']

            with self.lock:
                self.data.update(sensor_data)

            self._send_data()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def _send_data(self):
        topic = 'sensor/RadonAverage'
        data = self.data['radonShortTermAvg']
        self.data_sender.publish_data(topic, data)
