# Pico MicroPython Coursework

**Embedded-programming labs covering GPIO, RFID, Wi-Fi, HTTP dashboards and MQTT telemetry.**

Collected by Srun Sochettra for National University of Management, Year 2, Semester 2, as described in the original README. Examples use MicroPython, VS Code and MicroPico. This is a collection of independent exercises, not one deployable firmware application.

## Module guide

| Folder | Exercises |
| --- | --- |
| Module1_Pico_VSCode_MicroPython | LED blinking and internal-temperature calculation |
| Module2_Pico_RFID_VSCode | UID reading, RGB feedback, card block reads/writes and access checks |
| Module3_Getting_Started_with_Wi-Fi_MicroPython | Scanning, station connections, static addressing, AP fallback and LED dashboards |
| Module5_Webserver | Socket/asyncio servers, routes, JSON status and browser polling |
| Module6_MQTT_Protocol_&_IoT_Cloud_Integration | MQTT LED subscriptions and DHT22 telemetry |

The supplied numbering skips Module 4. Existing folders and lecture filenames are preserved.

## What the examples demonstrate

Module 1 includes an RP2040-labelled temperature formula, not calibrated ambient sensing. Module 2 has UID-only and UID-plus-card-text exercises; the secure filename is not evidence of production security.

Module 3's hybrid example tries station mode and falls back to an AP. Its dashboard polls status; the script labelled captive portal does not implement a DNS portal service.

Module 5 generates its displayed sensor values with random.randint. They are simulated values, not physical sensor readings. The AJAX example polls JSON status every three seconds. Module 6 reads a DHT22 on GP15; its v2 publisher also subscribes to LED commands but toggles the same LED in its loop.

This coursework is separate from the standalone pico-rfid-access-control repository.

## Run an exercise

The original README describes opening the repository in VS Code, connecting a board with appropriate MicroPython firmware, confirming MicroPico connectivity and using **MicroPico: Run Current File** for the selected script. This workflow was not executed during the refresh.

Run one exercise at a time. Inspect its imports and GPIO assignments first. Module 2 needs the corresponding local mfrc522.py; Module 5 imports SSID/PASSWORD from secrets.py; Module 6 needs config.py and its umqtt folder. Avoid flattening all modules onto the board because helper names overlap.

No firmware version or tested board matrix is supplied. Scripts mix Pin('LED'), Pin(25), RP2040-specific calculations and Pico 2 W descriptions. Do not assume every example runs unchanged on every Pico model.

## Configuration and safety

Review grounding/common reference, power, current limits and protection against the actual board/module specifications before wiring. This source is not a validated wiring design. Use a demonstration rig, not safety-critical equipment.

**Network credentials are committed in several Module 3 scripts and Module5_Webserver/secrets.py.** Some AP examples print passwords. If any values are live, rotate them with the network owner and clean public source/history appropriately. This overlay neither repeats nor removes them.

Module 6 config.py contains Wi-Fi/broker placeholders. Its client selects port 8883 when SSL is enabled and port is zero. SSL=True does not establish verified certificate validation or a tested connection. Review firmware compatibility and broker configuration separately.

Use only authorised cards and networks. The block-write exercise repeatedly writes block 1; use a disposable test card. HTTP controls have no application login or TLS configuration and should remain on an isolated lab network.

## Materials and attribution

The inventory includes lecture PDFs, Word documents and slides. Their binary contents were not inspected. Preserve attribution comments and confirm permissions before redistributing lectures or bundled drivers. No project licence file is supplied; this refresh assigns none.

## Checks and known gaps

All 38 supplied Python files passed CPython AST syntax parsing. No script was imported or executed. This does not verify MicroPython compatibility, wiring, network operation or sensor accuracy. No automated test suite is supplied; test_index.html is a page example, not a test runner.

Static review found mismatched RFID APIs in Intermediate/read_block.py, an undefined third-cascade driver method and a bitwise-complement condition in both drivers' polling loops. MQTT exercises import simple, not robust; the bundled robust client does not automatically enable reconnect behaviour.

Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) and [refresh notes](docs/repository-refresh.md). Firmware and configuration are unchanged.
