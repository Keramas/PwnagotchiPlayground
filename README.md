# PwnagotchiPlayground
Some scripts for Pwnagotchi

## Get Handshakes
Extracts all handshake data from Pwnagotchi. Dumps all hashes by type to aggregate file for easy cracking, and also zips all the handshakes to easy to export zip file.

Dependencies:
- cap2hccapx
- hcxpcaptool

Within the script, modify path to above binaries accordingly and set SSH key name for SCP.

## WiGLE It
Uses the WiGLE API to hunt down the exact location of APs discovered by the Pwnagotchi. (A WiGLE API key is required.) 

Feed it the AP name/MAC address and a latitude and longitude range. If located, it will generate a Google Maps link.

### Modes
- Mode 0: Parses indicated directory of saved PCAP files and performs a search on all of the APs gathered. (Warning: WiGLE API daily limitations may prevent this from finishing.)

- Mode 1: Looks up a single AP based on ESSID and BSSID.
