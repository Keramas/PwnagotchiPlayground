#!/bin/bash

#Globals to modify:
#-------------------------------------------------------------------------------------------
#Modify the location and/or SSH keyname for your Pwnagotchi.
key_path='~/.ssh/pwn.key'
#Modify regex to include other interface prefixes that are definitely not the Pwnagotchi.
pwn_interface=$(ip link | awk -F: '$0 !~ "lo|vm|enp|vir|eth0|wl|^[^0-9]"{print $2;getline}')
#Paths to cap2hccapx / hcxpcaptool
cap2hccapx_path='/opt/hashcat-utils/src/cap2hccapx.bin'
hcxpcaptool_path='/usr/local/bin/hcxpcaptool'
#-------------------------------------------------------------------------------------------
echo "[*] Checking for pwnagotchi interface..."
echo "[+] Found: $pwn_interface"
echo "[+] Setting IP address for SSH connection..."

ifconfig $pwn_interface 10.0.0.1 netmask 255.255.255.0 up
sleep 2
echo "[*] Connecting to pwnagotchi to download pcap data..."
scp -i $key_path root@10.0.0.2:/root/handshakes/* . &> /dev/null

echo "[+] Downloaded" $(ls -l *.pcap | wc -l) "pcaps."

echo "[*] Checking for PMKID data..."
for file in *.pcap; do
	$hcxpcaptool_path -z handshakes/pmkid/$file.pmkid $file &> /dev/null
done

echo "[*] Extracted" $(ls -l handshakes/pmkid/*.pmkid | wc -l) "PMKID hashes."

echo "[+] Checking for EAPOL data..."
for file in *.pcap; do
	$cap2hccapx_path $file handshakes/eapol/$file.hccapx &> /dev/null
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

#Aggregation of hashes into separate PMKID and EAPOL files
echo "[*] Aggregating EAPOL hashes into single file."
cat handshakes/eapol/*.hccapx > all_eapol_hashes.hccapx
echo "[*] EAPOL hashes placed in all_eapol_hashes.hccapx."
echo "[*] De-duping and aggregating PMKID hashes into single file."
cat handshakes/pmkid/*.pmkid | uniq -s 59 > all_pmkid_hashes.pmkid
echo "[*] PMKID hashes placed in all_pmkid_hashes.pmkid."

#Zip all hashes together into an exportable archive
echo "[+] Packaging all handshakes into zip"
now=$(date +"%Y_%m_%d-%H-%M-%S")
zip -r $now.handshakes.zip handshakes/ &> /dev/null

echo "[!] Finished!"
