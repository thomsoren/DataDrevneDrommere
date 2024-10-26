import os
from flask import Flask, json, render_template, flash
from requests import get, exceptions

app = Flask(__name__)

# Load UUID-to-user mappings
def load_uuid_mapping():
    try:
        data_file_path = os.path.join(os.path.dirname(__file__), 'data', 'uuid_user_mapping.json')
        with open(data_file_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        flash("Mapping file could not be loaded or found.", "danger")
        return {}

def fetch_connections():
    response = get("http://www.codexenmo.online:3000/api/proxy/http")
    response.raise_for_status() 
    data = response.json()
    
    # Load the mapping once
    uuid_mapping = load_uuid_mapping()
    
    # Apply mappings
    for proxy in data.get("proxies", []):
        uuid = proxy.get("UUID")
        if uuid in uuid_mapping:
            # Add user-friendly name and location, or modify as needed
            proxy["user"] = uuid_mapping[uuid].get("user", "Unknown User")
            proxy["location"] = uuid_mapping[uuid].get("location", "Unknown Location")
    
    return data

@app.route("/index")
def index():
    try:
        data = fetch_connections()
    except exceptions.RequestException as e:
        flash(f"An error occurred while fetching proxy data: {e}", "danger")
        data = {"proxies": []}
    
    if not data.get("proxies"):
        flash("No proxies found.", "warning")
    
    return render_template('index.html', proxies=data.get("proxies", []))


@app.route("/")
def signin():
    return render_template('sign_in.html')

@app.route('/reset_proxy/<proxy_name>')
def reset_proxy(proxy_name):
    # Implement the reset logic here
    flash(f"Proxy '{proxy_name}' has been reset.", "success")
    return index()

@app.route('/stop_proxy/<proxy_name>')
def stop_proxy(proxy_name):
    # Implement the stop logic here
    flash(f"Proxy '{proxy_name}' has been stopped.", "danger")
    return index()

if __name__ == "__main__":
    app.run(debug=True)