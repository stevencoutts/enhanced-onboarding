# Enhanced Onboarding Watcher

A lightweight Python app that monitors interface link-up events on a Cisco Catalyst 9000 switch via RESTCONF and triggers onboarding workflows automatically. Designed for deployment as a Docker container, including on the switch itself using Cisco IOx.

---

## Features
- Polls switch interfaces for link-up events using RESTCONF
- Detects newly active ("up") interfaces
- Triggers onboarding via a customizable RESTCONF API call
- Configurable via environment variables
- Logging and error handling included

---

## Requirements
- Cisco Catalyst 9000 series switch (with IOx support, e.g., C9300, C9400, C9500, C9600)
- IOS-XE 16.10+ (IOx and RESTCONF support)
- DNA Advantage or Premier license
- Docker (for local build/testing)
- Python 3.7+

---

## Configuration

The app is configured via environment variables:

| Variable         | Description                        | Default        |
|------------------|------------------------------------|---------------|
| `SWITCH_IP`      | Switch IP address or hostname      | 10.1.1.1      |
| `SWITCH_USER`    | RESTCONF username                  | admin         |
| `SWITCH_PASS`    | RESTCONF password                  | C1sco12345    |
| `POLL_INTERVAL`  | Polling interval (seconds)         | 5             |

---

## RESTCONF Endpoint Customization

The onboarding trigger endpoint and payload in `watcher.py` are placeholders:

```python
url = f"{BASE_URL}/xyz-enhanced-onboard:onboard"  # <-- Placeholder endpoint
payload = {"interface": iface}  # <-- Placeholder payload
```

**Update these to match your switch's YANG model or API.**

---

## Build & Run Locally

1. **Clone the repo and enter the directory:**
   ```sh
   git clone <your-repo-url>
   cd Enhanced\ Onboarding/app
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set environment variables and run:**
   ```sh
   export SWITCH_IP=10.1.1.1
   export SWITCH_USER=admin
   export SWITCH_PASS=C1sco12345
   python watcher.py
   ```

---

## Build & Deploy as Docker Container

1. **Build the Docker image:**
   ```sh
   docker build -t enhanced-onboarding:latest .
   ```
2. **Run the container:**
   ```sh
   docker run -e SWITCH_IP=10.1.1.1 -e SWITCH_USER=admin -e SWITCH_PASS=C1sco12345 enhanced-onboarding:latest
   ```

---

## Deploy on Catalyst 9000 (IOx)

1. **Install IOx Client:**
   ```sh
   pip install ioxclient
   ```
2. **Create IOx app skeleton:**
   ```sh
   ioxclient application init enhanced-onboarding
   cd enhanced-onboarding
   ```
3. **Save Docker image and copy:**
   ```sh
   docker save enhanced-onboarding:latest -o enhanced-onboarding.tar
   cp ../enhanced-onboarding.tar .
   ```
4. **Edit `package.yaml` as needed.**
5. **Package the app:**
   ```sh
   ioxclient application package .
   ```
6. **Copy the package to the switch (via SCP or WebUI).**
7. **Install and activate via switch CLI:**
   ```sh
   app-hosting install appid enhanced-onboarding package flash:enhanced-onboarding.tar
   app-hosting activate appid enhanced-onboarding
   app-hosting start appid enhanced-onboarding
   ```
8. **Check status and logs:**
   ```sh
   show app-hosting list
   app-hosting logs appid enhanced-onboarding
   ```

---

## Local Development with Python Virtual Environments

It is recommended to use a Python virtual environment (`venv`) for local development to isolate dependencies and avoid conflicts with system packages.

### Create and Activate a Virtual Environment

1. **Create the virtual environment:**
   ```sh
   python3 -m venv venv
   ```
2. **Activate the environment:**
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
3. **Install dependencies:**
   ```sh
   pip install -r app/requirements.txt
   ```

When finished, you can deactivate the environment with:
```sh
deactivate
```

**Note:** Using `venv` is only necessary for local development. It is not required inside Docker containers or when running on the switch via IOx, as those environments are already isolated.

---

## Local Testing with a Mock RESTCONF Server

You can test the watcher app without a real switch by running a mock RESTCONF server using Flask. This simulates the required RESTCONF endpoints.

### 1. Install Flask (for local testing only)

```
pip install flask
```

Or add `flask` to your `requirements.txt` (for local testing only).

### 2. Run the Mock Server

```
python mock_switch.py
```

This will start a server on `localhost:6000` that simulates the RESTCONF API.

### 3. Point the Watcher to the Mock Server

Set the environment variable before running the watcher:

```
export SWITCH_IP=localhost:6000
```

### 4. Run the Watcher

```
python app/watcher.py
```

The watcher will interact with the mock server as if it were a real switch. You can modify `mock_switch.py` to simulate different interface states or onboarding scenarios.

---

## Troubleshooting
- **SSL Errors:** The app disables SSL verification for demo purposes. For production, use valid certificates.
- **RESTCONF 401/403:** Check credentials and RESTCONF enablement on the switch.
- **No onboarding triggered:** Ensure the RESTCONF endpoint and payload match your switch's YANG model.
- **Resource errors on switch:** Check available CPU/memory for IOx containers.

---

## License
MIT
