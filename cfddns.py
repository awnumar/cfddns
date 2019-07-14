#!/usr/bin/env python

import json
import requests
import sys
import time

# Declare Cloudflare-specific API values
endpoint = "https://api.cloudflare.com/client/v4/"
cf_auth = {
    "Content-Type": "application/json",
    "X-Auth-Key": "", # User specified
    "X-Auth-Email": "",
}

def get_external_ip():
    return requests.get("https://api.ipify.org/").text

def get_zone_id(zone):
    return requests.get(endpoint + "zones", params={"name": zone}, headers=cf_auth).json()["result"][0]["id"]

def get_record_id(record, zone_id):
    return requests.get(endpoint + "zones/" + zone_id + "/dns_records", params={"name": record}, headers=cf_auth).json()["result"][0]["id"]

def update_record_ip(record, record_id, zone_id, ip_address):
    return requests.put(endpoint + "zones/" + zone_id + "/dns_records/" + record_id, data=json.dumps({
        "type": "A",
        "name": record,
        "content": ip_address,
        "ttl": 1,
        "proxied": False,
    }), headers=cf_auth).json()["success"]

def update(zone, record, email, api_key):
    # Setup API authentication values
    global cf_auth
    cf_auth["X-Auth-Key"] = api_key
    cf_auth["X-Auth-Email"] = email

    # Grab record and zone identification strings
    zone_id = get_zone_id(zone)
    record_id = get_record_id(record, zone_id)

    # Grab external IPv4 address
    ip_address = get_external_ip()

    # Sumbit IP update request to the Cloudflare API
    if update_record_ip(record, record_id, zone_id, ip_address):
        return time.ctime(time.time()) + ": " + ip_address

def main():
    # Verify the number of arguments
    if len(sys.argv) != 5:
        print(f"usage: {sys.argv[0]} zone record email api_key\n       {sys.argv[0]} example.com ssh.example.com me@example.com 0123456789abcdef")
        return

    # Run ip update routine
    result = update(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    if result:
        print(result)
    else:
        print("Update procedure failed")

if __name__ == "__main__":
    main()
