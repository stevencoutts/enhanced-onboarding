import os
import time
import requests
import logging

# Disable SSL warnings for demo purposes (not recommended for production)
requests.packages.urllib3.disable_warnings()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Configuration from environment variables
SWITCH = os.environ.get('SWITCH_IP', '10.1.1.1')
USER = os.environ.get('SWITCH_USER', 'admin')
PASS = os.environ.get('SWITCH_PASS', 'C1sco12345')
POLL_INTERVAL = int(os.environ.get('POLL_INTERVAL', '5'))  # seconds

# RESTCONF base URL
BASE_URL = f"https://{SWITCH}/restconf/data"

# RESTCONF headers
HEADERS = {
    'Accept': 'application/yang-data+json',
    'Content-Type': 'application/yang-data+json',
}

def get_up_interfaces():
    """Poll the switch for interfaces with oper-status 'up'."""
    url = f"{BASE_URL}/ietf-interfaces:interfaces-state"
    try:
        resp = requests.get(url, auth=(USER, PASS), headers=HEADERS, verify=False, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        interfaces = data.get('interfaces-state', {}).get('interface', [])
        up_ifaces = [i['name'] for i in interfaces if i.get('oper-status') == 'up']
        return up_ifaces
    except Exception as e:
        logging.error(f"Failed to get interface states: {e}")
        return []

def onboard_interface(iface):
    """Trigger onboarding for a given interface (placeholder endpoint and payload)."""
    # TODO: Replace with the actual onboarding endpoint and payload for your environment
    url = f"{BASE_URL}/xyz-enhanced-onboard:onboard"  # <-- Placeholder endpoint
    payload = {"interface": iface}  # <-- Placeholder payload
    try:
        resp = requests.post(url, json=payload, auth=(USER, PASS), headers=HEADERS, verify=False, timeout=5)
        if resp.status_code in (200, 201, 204):
            logging.info(f"Onboarding triggered for {iface} (status {resp.status_code})")
        else:
            logging.warning(f"Onboarding failed for {iface}: {resp.status_code} {resp.text}")
    except Exception as e:
        logging.error(f"Error onboarding {iface}: {e}")

def main():
    prev_up = set()
    logging.info(f"Starting Enhanced Onboarding watcher for switch {SWITCH}")
    while True:
        current_up = set(get_up_interfaces())
        new_up = current_up - prev_up
        for iface in new_up:
            logging.info(f"[+] New link-up detected: {iface}, triggering onboarding…")
            onboard_interface(iface)
        prev_up = current_up
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main() 