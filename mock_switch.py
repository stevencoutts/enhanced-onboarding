from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated interface state (customize as needed)
interfaces_state = {
    "interfaces-state": {
        "interface": [
            {"name": "GigabitEthernet1/0/1", "oper-status": "up"},
            {"name": "GigabitEthernet1/0/2", "oper-status": "down"},
        ]
    }
}

@app.route('/restconf/data/ietf-interfaces:interfaces-state', methods=['GET'])
def get_interfaces_state():
    return jsonify(interfaces_state)

@app.route('/restconf/data/xyz-enhanced-onboard:onboard', methods=['POST'])
def onboard():
    data = request.json
    print(f"Received onboarding request: {data}")
    return '', 204  # Simulate success

if __name__ == '__main__':
    app.run(port=5000) 