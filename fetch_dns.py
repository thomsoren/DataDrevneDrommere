from flask import Flask, render_template, abort, flash
import os
from domeneshop import Client
from dotenv import load_dotenv
import requests
import base64
import json
from DNS_mapper import get_domain_list

load_dotenv()

app = Flask(__name__)

# Retrieve the API token and secret from environment variables
TOKEN = os.getenv('TOKEN') 
SECRET = os.getenv('SECRET')

if not TOKEN: raise ValueError("No Domeneshop API key found. Please set the DOMENESHOP_API_KEY environment variable.")
if not SECRET:
    raise ValueError("No Domeneshop API secret found. Please set the DOMENESHOP_SECRET environment variable.")

# Initialize the Domeneshop client
client = Client(TOKEN, SECRET)

API_BASE_URL = "https://api.domeneshop.no/v0"

credentials = f"{TOKEN}:{SECRET}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/json'
}

@app.route("/")
def hello_world():
    domains = get_domain_list(API_BASE_URL, headers)
    
    if not domains:
        message = "No domains found."
        return render_template('index.html', domains=[], message=message)
    
    # Filter for 'codexenmo.online'
    target_domain = "codexenmo.online"
    filtered_domains = [domain for domain in domains if domain['domain'] == target_domain]
    
    if not filtered_domains:
        flash(f"Domain '{target_domain}' not found.", "warning")
    
    # Render the HTML template with forwards data
    return render_template('index.html', domains = filtered_domains)

if __name__ == "__main__":
    app.run(debug=True)