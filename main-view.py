import requests

# Replace these with your actual User ID and Secret key
USER_ID = '98639827-XXXX-XXXX-XXXX-323523ebbaa3'
SECRET_KEY = 'ac6db57a-XXXX-XXXX-XXXX-dc7bf905d80e'
DEVICE_ID = 'XXXXXXXXXX'  # Replace with your actual device ID

# Step 1: Generate an Access Token
token_url = 'https://accounts-api.airthings.com/v1/token'
token_data = {
    'grant_type': 'client_credentials',
    'client_id': USER_ID,
    'client_secret': SECRET_KEY
}

response = requests.post(token_url, json=token_data)
response.raise_for_status()  # Raise an error for bad status codes
token_info = response.json()
access_token = token_info['access_token']

# Step 2: Fetch the Latest Sensor Data
data_url = f'https://ext-api.airthings.com/v1/devices/{DEVICE_ID}/latest-samples'
headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(data_url, headers=headers)
response.raise_for_status()  # Raise an error for bad status codes
sensor_data = response.json()

print(sensor_data)