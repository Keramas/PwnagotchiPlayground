#!/usr/bin/python3

import requests
import argparse
import json
import sys
import os

wigleURL="https://api.wigle.net/api/v2/network/search?"
token = "ADD YOUR WIGLE API BASIC AUTH KEY HERE"

essid_list = []
bssid_list = []

def get_args():
    parser = argparse.ArgumentParser(description="Find an AP location with Wigle API", epilog="Wigle it, just a little bit!\n")
    parser.add_argument('-m', '--mode', type=str, help="Select either 0 or 1. 0 is directory mode, whereas 1 is single query mode.", required=True)
    parser.add_argument('-hm', '--latmin', type=str, help="", required=True)
    parser.add_argument('-hM', '--latmax', type=str, help="", required=True)
    parser.add_argument('-vm', '--longmin', type=str, help="", required=True)
    parser.add_argument('-vM', '--longmax', type=str, help="", required=True) 
    parser.add_argument('-d', '--directory', type=str, help="", required=False)
    parser.add_argument('-e', '--essid', type=str, help="", required=False)
    parser.add_argument('-b', '--bssid', type=str, help="", required=False)

    args = parser.parse_args()
    mode = args.mode
    directory = args.mode
    latmin = args.latmin
    latmax = args.latmax
    longmin = args.longmin
    longmax = args.longmax
    essid = args.essid
    bssid = args.bssid

    return mode,directory,latmin,latmax,longmin,longmax,essid,bssid


def parseFiles(directory):
    for file in os.listdir(directory):
        essid = file.split(".")[0].split("_")[0]    
        bssid = file.split(".")[0].split("_")[1]
        bssid_mac = ':'.join([bssid[i:i+2] for i in range(0, len(bssid), 2)])
        essid_list.append(essid)
        bssid_list.append(bssid_mac)


def search(latmin,latmax,longmin,longmax,essid,bssid):
    headers = {"authorization":"Basic "+token, "Accept":"application/json"}
    query = wigleURL+"latrange1="+latmin+"&latrange2="+latmax+"&longrange1="+longmin+"&longrange2="+longmax+"&ssid="+essid+"&netid="+bssid
    s = requests.get(query, headers=headers)
    print(s.content)
    return s.json() 


def parseResults(results):

    total = results["totalResults"]

    if total == 0:
        print("[-] AP was not found. :(")
        sys.exit(0)

    else:
        print("[+] AP found. Parsing data...")

        latitude = results["results"][0]["trilat"]
        longitude = results["results"][0]["trilong"]
        ssid = results["results"][0]["ssid"]
        maplink = "https://www.google.com/maps/search/?api=1&query="+str(latitude)+","+str(longitude)

        print("SSID -", str(ssid))
        print("-----------------------")
        print("Longitude:", str(longitude))
        print("Latitude:", str(latitude)) 
        print("Google maps link:",maplink)
        print("-----------------------")
        print("\n")


def main():
    latmin,latmax,longmin,longmax,essid,bssid,directory,mode = get_args()

    if mode == 0:
        parseFiles(directory)
        for i in essid_list:
            for j in bssid_list:
                results = search(latmin,latmax,longmin,longmax,i,j)
                parseResults(results)

    elif mode == 1:
        results = search(latmin,latmax,longmin,longmax,essid,bssid)
        parseResults(results)

    else:
        print("[!] Mode not selected. Please select either mode 0 or mode 1.")
        sys.exit(0)


if __name__ == "__main__":
    main()
    print("[!] Done.")
    sys.exit(0)
