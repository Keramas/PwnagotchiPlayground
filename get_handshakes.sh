#!/bin/bash
pwn_interface=$(ip link | awk -F: '$0 !~ "lo|vir|eth0|wl|^[^0-9]"{print $2;getline}')

echo "[*] Checking for pwnagotchi interface..."
echo "[+] Found: $pwn_interface"
echo "[+] Setting IP address for SSH connection..."

ifconfig $pwn_interface 10.0.0.1 netmask 255.255.255.0 up
sleep 2
echo "[*] Connecting to pwnagotchi to download pcap data..."
scp -i ~/.ssh/pwn.key root@10.0.0.2:/root/handshakes/* . &> /dev/null

echo "[+] Downloaded" $(ls -l *.pcap | wc -l) "pcaps."

echo "[*] Checking for PMKID data..."
for file in *.pcap; do
	hcxpcaptool -z handshakes/pmkid/$file.pmkid $file &> /dev/null
done

echo "[*] Extracted" $(ls -l handshakes/pmkid/*.pmkid | wc -l) "PMKID hashes."

echo "[+] Checking for EAPOL data..."
for file in *.pcap; do
	/opt/hashcat-utils/src/cap2hccapx.bin $file handshakes/eapol/$file.hccapx &> /dev/null
done

echo "[*] Checking for valid handshakes..."

for file in handshakes/eapol/*.hccapx; do
	if [ -s $file ]
	then
		continue
	else
		rm $file
	fi
done

echo "[*] Extracted" $(ls -l handshakes/eapol/*.hccapx | wc -l) "EAPOL hashes."

echo "[+] Cleaning up pcaps"
rm *.pcap

echo "[+] Packaging handshakes into zip"
now=$(date +"%m_%d_%Y")
zip -r $now.handshakes.zip handshakes/ &> /dev/null
