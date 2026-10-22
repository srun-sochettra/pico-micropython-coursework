# Contributing

Keep changes focused on independent coursework exercises. Preserve module numbering, lecture files and existing attribution.

Identify the exact script, board, firmware, helper files and pin configuration. Do not import scripts indiscriminately: many start infinite loops, connect to networks or write cards at module load.

For RFID changes, check the selected driver's API using disposable authorised cards. For HTTP changes, check unknown routes, malformed requests, disconnects and repeated polling on an isolated network. For MQTT changes, verify topic/payload types, connection loss, TLS configuration and subscriber receipt with a controlled broker.

Distinguish simulated values from sensor measurements, syntax parsing from hardware execution and publish calls from confirmed receipt. Report checks actually performed and remaining gaps.

Describe the exercise, focused change and hardware/network impact in pull requests. Never commit real passwords, broker credentials, personal card identifiers or private logs. See [SECURITY.md](SECURITY.md).
