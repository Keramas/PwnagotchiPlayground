#!/usr/bin/python3

import requests
import argparse
import json
import sys

wigleURL="https://api.wigle.net/api/v2/network/search?"
token = "ADD YOUR WIGLE API BASIC AUTH KEY HERE"

def get_args():
    parser = argparse.ArgumentParser(description="Find an AP location with Wigle API", epilog="Wigle it, just a little bit!\n")
    parser.add_argument('-hm', '--latmin', type=str, help="", required=True)
    parser.add_argument('-hM', '--latmax', type=str, help="", required=True)
    parser.add_argument('-vm', '--longmin', type=str, help="", required=True)
    parser.add_argument('-vM', '--longmax', type=str, help="", required=True)
    parser.add_argument('-e', '--essid', type=str, help="", required=True)
    parser.add_argument('-b', '--bssid', type=str, help="", required=True)

    args = parser.parse_args()
    latmin = args.latmin
    latmax = args.latmax
    longmin = args.longmin
    longmax = args.longmax
    essid = args.essid
    bssid = args.bssid

    return latmin,latmax,longmin,longmax,essid,bssid


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
    latmin,latmax,longmin,longmax,essid,bssid = get_args()
    print("[+] Querying Wigle for data...")
    results = search(latmin,latmax,longmin,longmax,essid,bssid)
    print("[+] AP found. Parsing results...")    
    parseResults(results)


if __name__ == "__main__":
    main()
