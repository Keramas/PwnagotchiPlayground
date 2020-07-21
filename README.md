# PwnagotchiPlayground
Suite of scripts to make Pwnagotchi data extraction and parsing easier.

## Get Handshakes
Extracts all handshake data from Pwnagotchi. Dumps all hashes by type to aggregate file for easy cracking, and also zips all the handshakes to easy to export zip file.

Dependencies:
- [cap2hccapx](https://hashcat.net/wiki/doku.php?id=hashcat_utils)
- [hcxpcaptool](https://github.com/ZerBea/hcxtools)

### How to use
Within the script, modify the global variables at the top to suppoly proper paths to the above binaries, as well as paths to the SSH key for the Pwnagotchi. Depending on your Linux environment, modification of the regex for determining the Pwnagotchi interface may be required as well. 

Unless the user executing the script has permissions to modify interface settings, sudo execution will be necessary.

<img src = "images/gethandshakes.png">

## WiGLE It
Uses the WiGLE API to hunt down the exact location of APs discovered by the Pwnagotchi. (A WiGLE API key is required.) 

Feed it the AP name/MAC address and a latitude and longitude range. If located, it will generate a Google Maps link.

### Modes
- Mode 0: Parses indicated directory of saved PCAP files and performs a search on all of the APs gathered. 

Use the /handshakes/eapol/ or /handshakes/pmkid/ directories after running the get_handshakes script.

(Warning: WiGLE API daily limitations may prevent this from finishing if there are too many files.)
 
- Mode 1: Looks up a single AP based on ESSID and BSSID.
