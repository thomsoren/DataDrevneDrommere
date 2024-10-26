from flask import Flask, render_template, flash
from requests import get, exceptions

app = Flask(__name__)

def fetch_connections():
    response = get("http://www.codexenmo.online:3000/api/proxy/http")
    response.raise_for_status() 
    return response.json()

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