from flask import Flask, jsonify, request
import time
import random

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

# Track onboarded interfaces
onboarded = set()

@app.route('/restconf/data/ietf-interfaces:interfaces-state', methods=['GET'])
def get_interfaces_state():
    return jsonify(interfaces_state)

@app.route('/restconf/data/xyz-enhanced-onboard:onboard', methods=['POST'])
def onboard():
    data = request.json
    iface = data.get("interface")
    print(f"Received onboarding request: {data}")

    # Simulate random failure for demonstration
    if iface == "GigabitEthernet1/0/2":
        return "Simulated onboarding failure", 500

    # Simulate processing delay
    time.sleep(random.uniform(0.1, 0.5))

    # Mark as onboarded
    onboarded.add(iface)
    return '', 204  # Success

@app.route('/restconf/data/xyz-enhanced-onboard:status', methods=['GET'])
def onboarding_status():
    return jsonify({"onboarded": list(onboarded)})

if __name__ == '__main__':
    app.run(port=6000) 