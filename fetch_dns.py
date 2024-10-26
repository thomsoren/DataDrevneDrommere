import os

from flask import Flask, flash, json, jsonify, redirect, render_template
from requests import exceptions, get

GOOGLE_AUTH = True

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key


# Load UUID-to-user mappings once at startup
def load_uuid_mapping():
    try:
        data_file_path = os.path.join(
            os.path.dirname(__file__), "data", "uuid_user_mapping.json"
        )
        with open(data_file_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        flash("Mapping file could not be loaded or found.", "danger")
        return {}


uuid_mapping = load_uuid_mapping()


def fetch_connections():
    try:
        response = get("http://www.codexenmo.online:3000/api/proxy/http")
        response.raise_for_status()
        data = response.json()
    except exceptions.RequestException as e:
        flash(f"Error fetching proxy data: {e}", "danger")
        return {
            "proxies": [],
            "total_online": 0,
            "total_offline": 0,
            "total_traffic_in": 0,
            "total_traffic_out": 0,
        }

    # Filter out www
    proxies = list(filter(lambda p: p["name"] != "www", data.get("proxies", [])))

    # Apply mappings
    for proxy in proxies:
        uuid = proxy.get("name")  # Use 'name' as the UUID key
        if uuid in uuid_mapping:
            proxy["user"] = uuid_mapping[uuid].get("user", "Unknown User")
            proxy["location"] = uuid_mapping[uuid].get("location", "Unknown Location")
        else:
            proxy["user"] = "Unknown User"
            proxy["location"] = "Unknown Location"

    # Compute summary statistics
    total_online = sum(1 for proxy in proxies if proxy.get("status") == "online")
    total_offline = sum(1 for proxy in proxies if proxy.get("status") == "offline")
    total_traffic_in = sum(proxy.get("todayTrafficIn", 0) for proxy in proxies)
    total_traffic_out = sum(proxy.get("todayTrafficOut", 0) for proxy in proxies)

    return {
        "proxies": proxies,
        "total_online": total_online,
        "total_offline": total_offline,
        "total_traffic_in": total_traffic_in,
        "total_traffic_out": total_traffic_out,
    }


@app.route("/data")
def getData():
    data = fetch_connections()
    if data is None:
        return (
            jsonify({"error": "Failed to fetch data."}),
            500,
        )  # 500 Internal Server Error

    return jsonify({"proxies": data.get("proxies", [])}), 200  # 200 OK


@app.route("/index")
def index():
    data = fetch_connections()

    if not data.get("proxies"):
        flash("No proxies found.", "warning")

    locations = [
        {"name": "Oslo", "lat": 59.9139, "lng": 10.7522},
        {"name": "Bergen", "lat": 60.3913, "lng": 5.3221},
        {"name": "Trondheim", "lat": 63.4305, "lng": 10.3951},
        {"name": "Stavanger", "lat": 58.9690, "lng": 5.7331},
        {"name": "Tromsø", "lat": 69.6492, "lng": 18.9553},
        ]
    return render_template(
        "index.html",
        proxies=data.get("proxies", []),
        total_online=data.get("total_online", 0),
        total_offline=data.get("total_offline", 0),
        total_traffic_in=data.get("total_traffic_in", 0),
        total_traffic_out=data.get("total_traffic_out", 0),locations=json.dumps(locations)
    )


@app.route("/")
def signin():
    if not GOOGLE_AUTH:
        return redirect("/index")

    return render_template("sign_in.html")


@app.route("/reset_proxy/<proxy_name>")
def reset_proxy(proxy_name):
    # Implement the reset logic here
    flash(f"Proxy '{proxy_name}' has been reset.", "success")
    return index()


@app.route("/stop_proxy/<proxy_name>")
def stop_proxy(proxy_name):
    # Implement the stop logic here
    flash(f"Proxy '{proxy_name}' has been stopped.", "danger")
    return index()


@app.route("/map")
def getmap():
    locations = [
        {"name": "Oslo", "lat": 59.9139, "lng": 10.7522},
        {"name": "Bergen", "lat": 60.3913, "lng": 5.3221},
        {"name": "Trondheim", "lat": 63.4305, "lng": 10.3951},
        {"name": "Stavanger", "lat": 58.9690, "lng": 5.7331},
        {"name": "Tromsø", "lat": 69.6492, "lng": 18.9553},
    ]
    return render_template("map.html", locations=json.dumps(locations))


if __name__ == "__main__":
    app.run(debug=True)
