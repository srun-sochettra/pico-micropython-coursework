# Security and lab-use guidance

These are educational examples, not hardened services. No security audit, supported-version programme or reporting deadline is established here.

## Committed configuration

Several Module 3 scripts and Module5_Webserver/secrets.py contain network credentials. Some AP examples print passwords. Their validity is unknown. If live, rotate them with the responsible owner and review public history/exports. A secrets.py filename does not protect committed contents.

No .gitignore is included in the supplied inventory. Review staged files and add appropriate exclusions as a separate change before storing private configuration. This overlay does not edit credentials or erase history.

## Network and hardware boundaries

HTTP examples accept unauthenticated requests and change LED state through GET routes. Do not expose them to the public internet or use them to control hazardous equipment.

MQTT scripts enable SSL but do not establish a verified certificate-trust configuration. Several share fixed client IDs and topics. The practice scripts import umqtt.simple rather than the bundled robust client.

Use only authorised disposable cards. Block-write exercises alter card contents. UID/name comparisons and default block keys do not establish a production identity system.

Review grounding, power and protective components before connecting hardware. No electrical or physical safety validation was performed here.

## Reporting

Redact passwords, card identifiers and private network details. Use a verified private maintainer channel if available, or request one without publishing sensitive details. No dedicated reporting address or enabled private-reporting feature was confirmed.
