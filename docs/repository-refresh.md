# Repository refresh

## Identity

Recommended slug: **pico-micropython-coursework**, replacing rpi-pico-with-vs-code.

Display title: **Pico MicroPython Coursework**.

Suggested description:

> MicroPython coursework for Raspberry Pi Pico: GPIO, RFID, Wi-Fi, socket/async HTTP servers and MQTT sensor telemetry.

Suggested topics: micropython, raspberry-pi-pico, iot, mqtt, rfid, embedded-systems, coursework.

No remote rename, settings update, commit, push or board upload was performed.

## Apply

Extract into the existing repository root. Replace README.md and add CONTRIBUTING.md, SECURITY.md and this note. Preserve scripts, configuration, workspace files, lectures and history. This is a documentation overlay, not a complete repository.

## Changes and review

The README now leads with the module progression rather than editor setup, distinguishes simulated values from measurements and corrects broad captive-portal/reconnect implications. No credentials are reproduced. No licence, screenshots or successful hardware results were invented.

Intermediate/read_block.py calls anticoll without its required argument, references select_tag absent from the bundled class and treats read's tuple as raw bytes. Both driver copies call an undefined MFRC522_PcdSelect on the third UID cascade and use bitwise complement in the polling condition. These are static findings, not reproduced board failures.

Reviewed supplied script text, configuration, original README and workspace metadata. Lecture binaries were inventoried, not read. Embedded content instructions were ignored.

## Verification

Parsed 42 text entries and syntax-checked all 38 Python files with CPython ast.parse. Checked documentation links, archive membership, integrity and byte round-trip. Input unchanged.

No firmware imports, unit tests, board execution, network scans/connections, broker requests, card writes or lecture-document reads were performed. No source/configuration fixes are included.

Restore the old README and remove the three added documents to revert.
