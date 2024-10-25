import requests
import json
import base64
import os
import sys

# Dine API-krav

API_BASE_URL = "https://api.domeneshop.no/v0"

# Opprett Basic Auth header
credentials = f"{TOKEN}:{SECRET}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/json'
}

def get_domains():
    url = f"{API_BASE_URL}/domains"
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")  # For feilsøking
    
    # Skriv responsen til en fil
    with open("response.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Response text skrevet til response.txt")
    
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Feil: Responsen er ikke gyldig JSON.")
            return None
    else:
        print(f"Feil ved henting av domener")
        return None


def find_domain_id(domain_name):
    domains = get_domains()
    if domains:
        for domain in domains:
            if domain['domain'] == domain_name:
                return domain['id']
    print(f"Domene ikke funnet.")
    return None

def add_dns_record(domain_id, host, record_type, data, ttl=3600):
    url = f"{API_BASE_URL}/domains/{domain_id}/dns"
    payload = {
        "host": host,
        "ttl": ttl,
        "type": record_type,
        "data": data
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        print(f"DNS-oppføring lagt til: {host}.{domain_id}")
        return response.json()
    else:
        print(f"Feil ved oppretting av DNS-oppføring: {response.status_code} - {response.text}")
        return None

def update_dns_record(domain_id, record_id, host, record_type, data, ttl=3600):
    url = f"{API_BASE_URL}/domains/{domain_id}/dns/{record_id}"
    payload = {
        "host": host,
        "ttl": ttl,
        "type": record_type,
        "data": data
    }
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print(f"DNS-oppføring oppdatert: {host}.{domain_id}")
        return response.json()
    else:
        print(f"Feil ved oppdatering av DNS-oppføring: {response.status_code} - {response.text}")
        return None

def delete_dns_record(domain_id, record_id):
    url = f"{API_BASE_URL}/domains/{domain_id}/dns/{record_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"DNS-oppføring med ID {record_id} slettet.")
    else:
        print(f"Feil ved sletting av DNS-oppføring: {response.status_code} - {response.text}")

def list_dns_records(domain_id):
    url = f"{API_BASE_URL}/domains/{domain_id}/dns"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Feil ved henting av DNS-oppføringer: {response.status_code} - {response.text}")
        return None

def test_api():
    
    url = f"{API_BASE_URL}/domains"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            print("API-kall vellykket. Her er domeneinformasjonen:")
            for domain in data:
                print(domain["domain"])
        except json.JSONDecodeError:
            print("Feil: Responsen er ikke gyldig JSON.")
    else:
        print(f"Feil ved API-kall: {response.status_code} - {response.text}")

if __name__ == "__main__":
    
    # Legg til en ny DNS-oppføring (A-oppføring for rpi1)
    domain_ID = "codexenmo.no"
    host = "rpi1"  # Subdomene, f.eks. rpi1.codexenmo.no
    record_type = "A"  # Type DNS-oppføring
    data = "192.168.0.1"  # IP-adressen du vil peke til
    ttl = 3600  # Valgfritt, standard er 3600 sekunder
    
    add_dns_record(domain_ID, host, record_type, data, ttl)
    test_api()