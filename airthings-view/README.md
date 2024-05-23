# Airthings View Plus API Integration

This project demonstrates how to integrate an ESP32 microcontroller with an Airthings View Plus device through the exposed REST API.

## Hardware

The Airthings View Plus is a smart air quality monitor that provides real-time radon readings, temperature, humidity, CO2, and TVOC levels. The device is battery-powered and communicates over Bluetooth Low Energy (BLE) during the configuration process and then over Wi-Fi once set up. The Airthings View Plus also has an exposed REST API that allows you to fetch the sensor data, which for example Home Assistant uses to integrate the device.

## How it works

The device is commissioned using the Airthings app, which connects to the device over BLE and configures the Wi-Fi settings. Once the device is connected to Wi-Fi, the measurements become visible in the Airthings app, in the web dashboard, and through the REST API. The REST API provides access to the current sensor data, as well as historical data.

### Device commissioning

Power on the device and download the Airthings app from the App Store or Google Play. Follow the instructions in the app to commission the device and connect it to your Wi-Fi network.

### REST API

To [start using the REST API](https://developer.airthings.com/docs/api/authorization#authorizing-through-code-flow), you need to obtain an API key. This can be done by logging in to the Airthings dashboard at [https://dashboard.airthings.com](https://dashboard.airthings.com/), then navigating to the `Integrations`->`API` tab and requesting an API key or `Secret key` as it is called in the platform. Once requested, it will take approximately 24 hours for the `Secret key` to be generated. It will be visible in the API tab once it is ready.

Both the `Secret key` and the `User ID` are in the UUID (Universally Unique Identifier) format and are required to authenticate with the REST API. The `User ID` can be found in the same `API` tab as the `Secret key`.

The following part of the documentation will show you how to use the REST API to fetch the sensor data from the Airthings View Plus device.

#### General API token

To generate an access token, you need to make a POST request to the `/v1/token` endpoint with the `User ID` and `Secret key` in the request body. The response will contain an access token that you can use to authenticate with the other endpoints.

POST `https://accounts-api.airthings.com/v1/token`

```json
{
  "grant_type": "client_credentials",
  "client_id": "98639827-XXXX-XXXX-XXXX-323523ebbaa3",
  "client_secret": "ac6db57a-XXXX-XXXX-XXXX-dc7bf905d80e"
}
```

and the response should look like this:

```json
{
  "access_token": "TOKEN",
  "token_type": "Bearer",
  "expires_in": 10800
}
```

#### Fetching sensor data

To fetch the sensor data, you need to make a GET request to the `/v1/devices/{device_id}/latest` endpoint with the access token in the `Authorization` header. The response will contain the latest sensor data for the specified device.

GET `https://ext-api.airthings.com/v1/devices/{device_id}/latest-samples`

```json
{
  "data": {
    "time": 1716466918,
    "battery": 100,
    "co2": 618.0,
    "humidity": 45.0,
    "pm1": 6.0,
    "pm25": 6.0,
    "pressure": 1016.5,
    "radonShortTermAvg": 16.0,
    "relayDeviceType": "hub",
    "temp": 25.8,
    "voc": 122.0
  }
}
```

For more endpoints and information, please refer to the [official Airthings API documentation](https://developer.airthings.com/docs/data-access) and the [business API documentation](https://ext-api.airthings.com/v1/api-docs/business).

### Integration with other platforms

Since a `Secret key` is required to generate a token for data access, it would be practical if the integrating platform (such as the esp32) had a way for the user to input the `Secret key` and `User ID`. This could for example be done by BLE. The platform could then use the `Secret key` and `User ID` to generate an access token and fetch the sensor data from the airthings server.
