# iotlab-pilotcase-radicair

Radicair manufactures and sells Radon fans that regulate indoor radon levels by exchanging contaminated air with fresh outdoor air while maintaining neutral pressure and recovering heat energy.

Radon is a radioactive gas that enters buildings in Sweden through construction materials like pre-1975 aerated concrete (blue concrete), as well as from the ground and household water. Sweden has some of the highest indoor radon levels in the world, with many homes exceeding 200 Bq/m³. The Swedish Radiation Safety Authority estimates that radon in dwellings causes around [500 lung cancer cases per year](https://www.stralsakerhetsmyndigheten.se/en/areas/radon/) in Sweden, most commonly among smokers. Radon is the second-most common cause of lung cancer after smoking, and long-term exposure to high levels of this odorless, invisible gas poses a serious health hazard. Approximately 15% of lung cancers in Sweden are induced by indoor radon in dwelling buildings.

## Hardware

In this project, we will take a look at how to integrate two Radon sensors from Airthings, more specifically Airthings Wave Plus and Airthings View Plus. The Airthings Wave Plus is a smart radon detector that provides real-time radon readings, temperature, humidity, CO2, and air pressure levels. The Airthings View Plus is a smart air quality monitor that provides real-time radon readings, temperature, humidity, CO2, and TVOC levels. Both devices are battery-powered and communicate over Bluetooth Low Energy (BLE).

<div align="center" width="100%">
<center>
  <table style="border-collapse: collapse" width="100%">
    <tr>
      <td
        valign="top"
        width="50%"
        style="border: 5px solid grey; padding: 10px"
      >
        <center>
        <br /><br /><br /><br />
          <img
            src="image.png"
            alt="Srcful Gateway"
            style="width=50% height=50%"
          /><br />
          <p align="center">
            Radon & air quality monitor with 7 sensors including radon, PM 2.5, CO2, and more<br /><br /><br />
            <a href="https://www.airthings.com/en/view-plus">View in store</a>
          </p>
        </center>
      </td>
      <td
        valign="top"
        width="50%"
        style="border: 5px solid grey; padding: 10px"
      >
        <center>
          <img
            src="image-1.png"
            alt="RAK Hotspot V2"
            style="width=50% height=50%"
          /><br />
          <p align="center">
            Bluetooth-enabled, smart monitor with 6 sensors measuring radon, CO2, VOCs and more.<br /><br /><br />
            <a href="https://www.airthings.com/en/wave-plus">View in store</a>
          </p>
        </center>
      </td>
    </tr>
  </table>
</center>
</div>

### Airthings Wave Plus

[This directory](/airthings-wave/) contains the information needed and code to link an ESP32 microcontroller to an Airthings Wave Plus device through Bluetooth Low Energy (BLE). The Airthings Wave Plus tracks indoor air quality for Radon, CO2, VOCs, Humidity, Temperature, and Air Pressure. Using this code, you can wirelessly fetch Humidity, Temperature, and Short Term/Long Term Radon levels with the ESP32.

A small [python script](/main-wave.py) is also included to demonstrate how to fetch the sensor data from the Airthings Wave Plus device using a computer.

### Airthings View Plus

[This directory](/airthings-view/) contains instructions for how to interact with the exposed REST API. The Airthings View Plus tracks indoor air quality for Radon, CO2, VOCs, Humidity, and Temperature. Using this code, you can wirelessly fetch Humidity, Temperature, and Radon levels with the ESP32.

A small [python script](/main-view.py) is also included to demonstrate how to fetch the sensor data from the Airthings View Plus device using the REST API.
