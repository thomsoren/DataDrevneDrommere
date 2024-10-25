import requests
import json
import base64
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Dine API-krav
TOKEN = os.getenv("TOKEN")
SECRET = os.getenv("SECRET")

print(TOKEN)
print(SECRET)

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

def get_dns_records(domain_id):
    # URL for fetching DNS records for a specific domain
    dns_url = f"{API_BASE_URL}/domains/{domain_id}/dns"
    response = requests.get(dns_url, headers=headers)
    
    if response.status_code == 200:
        try:
            dns_records = response.json()
            print(f"DNS oppføringer for domene ID {domain_id}:")
            for record in dns_records:
                print(f"Record ID: {record['id']}, Host: {record['host']}, Type: {record['type']}, Data: {record['data']}, TTL: {record['ttl']}")
            return dns_records
        except json.JSONDecodeError:
            print("Feil: Responsen er ikke gyldig JSON.")
            return None
    else:
        print(f"Feil ved henting av DNS-oppføringer: {response.status_code} - {response.text}")
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
    domain_id = find_domain_id(domain_id)
    url = f"{API_BASE_URL}/domains/{domain_id}/dns"
    payload = {
        "host": host,
        "ttl": ttl,
        "type": record_type,
        "data": data
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code)
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
    # Fetch list of domains
    url = f"{API_BASE_URL}/domains"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            print("API-kall vellykket. Her er domeneinformasjonen:")
            for domain in data:
                print(f"Domene: {domain['domain']} (ID: {domain['id']})")
            
            # Fetch DNS records for a specific domain (in this case, domain_id 2089158)
            domain_id = 2089158  # Replace with the desired domain ID
            dns_url = f"{API_BASE_URL}/domains/{domain_id}/dns"
            dns_response = requests.get(dns_url, headers=headers)

            if dns_response.status_code == 200:
                dns_data = dns_response.json()
                print(f"\nDNS oppføringer for domene ID {domain_id}:")
                for record in dns_data: # Her thomas kan du hente ut dataen du trenger
                    print(f"Record id: {record['id']} Host: {record['host']}, Type: {record['type']}, Data: {record['data']}, TTL: {record['ttl']}")
            else:
                print(f"Feil ved henting av DNS-oppføringer: {dns_response.status_code} - {dns_response.text}")
        
        except json.JSONDecodeError:
            print("Feil: Responsen er ikke gyldig JSON.")
    else:
        print(f"Feil ved API-kall: {response.status_code} - {response.text}")

def get_domain_list(api_base_url, headers):
    """
    Fetches a list of all domains and their DNS records from the API.

    Args:
        api_base_url (str): The base URL of the API.
        headers (Dict[str, str]): The headers to include in the API requests.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing domain and DNS record information.
    """
    domain_list = []
    
    # Fetch list of domains
    domains_url = f"{api_base_url}/domains"
    try:
        response = requests.get(domains_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching domains: {e}")
        return domain_list  # Return empty list on failure
    
    try:
        domains = response.json()
        print("API call successful. Here is the domain information:")
        for domain in domains:
            print(f"Domain: {domain.get('domain')} (ID: {domain.get('id')})")
            
            # Fetch DNS records for the current domain
            dns_url = f"{api_base_url}/domains/{domain.get('id')}/dns"
            try:
                dns_response = requests.get(dns_url, headers=headers)
                dns_response.raise_for_status()
                dns_records = dns_response.json()
                dns_list = []
                for record in dns_records:
                    dns_entry = {
                        'host': record.get('host'),
                        'type': record.get('type'),
                        'data': record.get('data'),
                        'ttl': record.get('ttl')
                    }
                    dns_list.append(dns_entry)
                domain_info = {
                    'domain': domain.get('domain'),
                    'id': domain.get('id'),
                    'dns_records': dns_list
                }
                domain_list.append(domain_info)
            except requests.RequestException as dns_err:
                print(f"Error fetching DNS records for domain ID {domain.get('id')}: {dns_err}")
            except json.JSONDecodeError:
                print(f"Error: DNS response for domain ID {domain.get('id')} is not valid JSON.")
    
        return domain_list
    
    except json.JSONDecodeError:
        print("Error: Domains response is not valid JSON.")
        return domain_list  # Return empty list on failure
    
if __name__ == "__main__":
    
    # Legg til en ny DNS-oppføring (A-oppføring for rpi1)
    domain_ID = "codexenmo.no"
    host = "gruppe4"  # Subdomene, f.eks. rpi1.codexenmo.no
    record_type = "A"  # Type DNS-oppføring
    data = "89.8.252.10"  # IP-adressen du vil peke til
    ttl = 3600  # Valgfritt, standard er 3600 sekunder
    
    # add_dns_record(domain_ID, host, record_type, data, ttl)
    get_dns_records(2089158)
    delete_dns_record(2089158, 6714538)
    get_dns_records(2089158)
    test_api()