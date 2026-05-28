# 🚀 Raspberry Pi Pico & MicroPython Coursework (NUM Y2 S2)

Central repository for my **Raspberry Pi Pico** coursework at the **National University of Management (NUM)**, Year 2, Semester 2. The labs use **MicroPython**, **VS Code**, and the **MicroPico** extension to practice embedded programming, sensors, networking, web servers, MQTT, and IoT cloud integration.

---

## 📂 Repository Structure

| Folder | Description | Key Topics |
| :--- | :--- | :--- |
| **`Module1_Pico_VSCode_MicroPython`** | Pico and MicroPython basics | GPIO, blinking LEDs, onboard temperature sensor |
| **`Module2_Pico_RFID_VSCode`** | RFID integration | SPI communication, MFRC522, RFID card reading/writing, access control |
| **`Module3_Getting_Started_with_Wi-Fi_MicroPython`** | Pico W networking | Wi-Fi scan/connect, static IP, AP mode, captive portal, dashboard |
| **`Module5_Webserver`** | Pico W web server practice | Sockets, HTTP routes, JSON responses, AJAX polling, sensor dashboards |
| **`Module6_MQTT_Protocol_&_IoT_Cloud_Integration`** | MQTT and IoT cloud integration | MQTT publish/subscribe, LED control, DHT22 telemetry, SSL broker connection |

---

## 🛠️ Development Environment

### Hardware

- Raspberry Pi Pico or Raspberry Pi Pico W
- USB-to-Micro-USB cable
- LEDs and resistors for GPIO practice
- MFRC522 RFID module for Module 2
- DHT22 sensor for MQTT telemetry practice

### Software

- [Visual Studio Code](https://code.visualstudio.com/)
- [MicroPico VS Code Extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go)
- MicroPython firmware for the correct board:
  - [Raspberry Pi Pico](https://micropython.org/download/RPI_PICO/)
  - [Raspberry Pi Pico W](https://micropython.org/download/RPI_PICO_W/)

---

## ⚙️ Quick Setup

1. Open this repository in VS Code.
2. Connect the Pico or Pico W by USB.
3. Flash the correct MicroPython UF2 firmware if the board is not already set up.
4. Confirm that the MicroPico extension shows the board as connected.
5. Open the script you want to run.
6. Run it with `Ctrl+Shift+P` -> `MicroPico: Run Current File`.

For scripts that import helper files, upload the full module folder or the required files to the board before running the main script.

---

## 🌐 Wi-Fi, Web Server, and MQTT Configuration

Networked examples require a **Raspberry Pi Pico W**.

### Wi-Fi examples

Module 3 and Module 5 scripts use the Pico W Wi-Fi interface for station mode, access point mode, web servers, and HTTP responses.

### MQTT examples

Module 6 uses MQTT over SSL with credentials stored in:

```text
Module6_MQTT_Protocol_&_IoT_Cloud_Integration/Practice/config.py
```

Update the placeholders before running MQTT scripts:

```python
wifi_ssid = 'REPLACE_WITH_YOUR_SSID'
wifi_password = 'REPLACE_WITH_YOUR_PASSWORD'
mqtt_server = b'MQTT_BROKER_URL'
mqtt_username = b'BROKER_USERNAME'
mqtt_password = b'BROKER_PASSWORD'
```

The `Practice/umqtt` folder contains the MQTT client library files used by the Module 6 scripts. Upload the `umqtt` folder with your selected MQTT script and `config.py`.

Common MQTT topics used in the practice scripts:

| Topic | Direction | Purpose |
| :--- | :--- | :--- |
| `pico/led` | Subscribe | Control the onboard LED with `ON` or `OFF` |
| `pico/temperature` | Publish | Send DHT22 temperature readings |
| `pico/humidity` | Publish | Send DHT22 humidity readings |

---

## 📘 Learning Resources

- [Pico MicroPython Lecture](./Module1_Pico_VSCode_MicroPython/Pico_VSCode_MicroPython_Lecture.pdf)
- [Pico RFID Lecture](./Module2_Pico_RFID_VSCode/Pico_RFID_VSCode_Lecture.pdf)
- [Pico W MQTT Lecture](./Module6_MQTT_Protocol_&_IoT_Cloud_Integration/Lecture/PicoW%20Getting%20Started%20with%20MQTT%20Lecture.pdf)

---

## 👨‍💻 Author

**Srun Sochettra**  
Year 2, Semester 2  
Course: Raspberry Pi Pico Development

---

> [!NOTE]
> This repository is for educational purposes. Code may need pin, Wi-Fi, and broker settings adjusted for your own hardware and network.
