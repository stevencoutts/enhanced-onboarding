from flask import Flask, jsonify, request
import time
import random
import threading

app = Flask(__name__)

# Simulated interface state
interfaces_state = {
    "interfaces-state": {
        "interface": [
            {"name": "GigabitEthernet1/0/1", "oper-status": "up"},
            {"name": "GigabitEthernet1/0/2", "oper-status": "down"},
        ]
    }
}

# Track onboarded interfaces and their MAC/IP
onboarded = {}

def simulate_mac_ip_learning(iface):
    # Simulate delay for MAC/IP learning
    time.sleep(random.uniform(1, 3))
    # Fake MAC and IP
    onboarded[iface]['mac'] = f"00:11:22:33:44:{random.randint(10,99)}"
    onboarded[iface]['ip'] = f"192.168.1.{random.randint(100,200)}"
    onboarded[iface]['status'] = "complete"

@app.route('/restconf/data/ietf-interfaces:interfaces-state', methods=['GET'])
def get_interfaces_state():
    return jsonify(interfaces_state)

@app.route('/restconf/data/xyz-enhanced-onboard:onboard', methods=['POST'])
def onboard():
    data = request.json
    iface = data.get("interface")
    mac = data.get("mac")
    ip = data.get("ip")
    print(f"Received onboarding request: {data}")

    if iface == "GigabitEthernet1/0/2":
        return "Simulated onboarding failure", 500

    # Simulate processing delay
    time.sleep(random.uniform(0.1, 0.5))

    # Start with status 'pending'
    onboarded[iface] = {
        "status": "pending",
        "mac": mac,
        "ip": ip
    }

    # If MAC/IP not provided, simulate learning them asynchronously
    if not mac or not ip:
        threading.Thread(target=simulate_mac_ip_learning, args=(iface,)).start()
    else:
        onboarded[iface]['status'] = "complete"

    return '', 204  # Success

@app.route('/restconf/data/xyz-enhanced-onboard:status', methods=['GET'])
def onboarding_status():
    return jsonify({"onboarded": onboarded})

@app.route('/restconf/data/xyz-enhanced-onboard:inject', methods=['POST'])
def inject_mac_ip():
    data = request.json
    iface = data.get("interface")
    mac = data.get("mac")
    ip = data.get("ip")
    if iface in onboarded:
        onboarded[iface]['mac'] = mac
        onboarded[iface]['ip'] = ip
        onboarded[iface]['status'] = "complete"
        return '', 204
    else:
        return "Interface not onboarded", 404

if __name__ == '__main__':
    app.run(port=6000) 