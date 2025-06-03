import subprocess
import requests
import time
import re
import os
import json
import dotenv

config = dotenv.dotenv_values()
LOG_FILE = "/var/log/nginx/access.log"  # Or your Apache log
VT_API_KEY = config.get("VIRUS_TOTAL_API_KEY", None)
THRESHOLD = 5  # Minimum malicious detections to trigger block
CHECKED_IPS = set()
RATE_LIMIT_DELAY = 3  # seconds
OUTPUT_JSON = "/home/dqrk/vt/malicious_ips_by_asn.json"
IP_REGEX = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3})")

asn_ip_map = {}

def load_existing_json():
    """Load existing data from JSON if it exists."""
    global asn_ip_map
    if os.path.exists(OUTPUT_JSON):
        try:
            with open(OUTPUT_JSON, "r") as f:
                data = json.load(f)
                for entry in data:
                    asn = str(entry.get("asn"))
                    ips = entry.get("ips", [])
                    if asn:
                        asn_ip_map[asn] = list(set(asn_ip_map.get(asn, []) + ips))
            print(f"[+] Loaded existing data from {OUTPUT_JSON}")
        except Exception as e:
            print(f"[!] Failed to load existing JSON: {e}")

def save_json():
    """Save ASN-IP mapping to a JSON file."""
    formatted = [
        {
            "type": "asn",
            "asn": str(asn),
            "ips": sorted(ips)
        } for asn, ips in asn_ip_map.items()
    ]
    with open(OUTPUT_JSON, "w") as f:
        json.dump(formatted, f, indent=4)
    print(f"[+] Saved data to {OUTPUT_JSON}")

def add_ip_to_asn(asn, ip):
    """Add IP to the ASN group in the map."""
    if asn not in asn_ip_map:
        asn_ip_map[asn] = []
    if ip not in asn_ip_map[asn]:
        asn_ip_map[asn].append(ip)
        return True
    return False

def check_ip(ip):
    try:
        response = requests.get(
            f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
            headers={"x-apikey": VT_API_KEY}
        )
        if response.status_code != 200:
            print(f"[!] Error from VirusTotal for {ip}: {response.status_code}")
            return

        data = response.json()
        attributes = data.get("data", {}).get("attributes", {})
        malicious_count = attributes.get("last_analysis_stats", {}).get("malicious", 0)
        asn = str(attributes.get("asn", ""))

        print(f"[*] {ip} => {malicious_count} engines flagged it as malicious. ASN: {asn}")
        if malicious_count >= THRESHOLD and asn:
            if add_ip_to_asn(asn, ip):
                save_json()

    except Exception as e:
        print(f"[!] Failed to check {ip}: {e}")

def tail_log():
    print("[*] Starting log monitor...")
    try:
        with subprocess.Popen(["tail", "-F", LOG_FILE], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True) as proc:
            for line in proc.stdout:
                print(line)
                match = IP_REGEX.search(line)
                if match:
                    ip = match.group(1)
                    if ip.startswith("127.") or ip in CHECKED_IPS:
                        continue
                    CHECKED_IPS.add(ip)
                    check_ip(ip)
                    time.sleep(RATE_LIMIT_DELAY)
    except KeyboardInterrupt:
        print("\n[!] Exiting...")
        save_json()

if __name__ == "__main__":
    load_existing_json()
    tail_log()