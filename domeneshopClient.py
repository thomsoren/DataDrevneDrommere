import json
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

class DomeneshopClient:
    """
    A client for interacting with the Domeneshop API to manage domains and DNS records.
    """
    
    def __init__(self, token, secret, domain_name="codexenmo.online", record_type="A", base_url="https://api.domeneshop.no/v0"):
        """
        Initialize the DomeneshopClient.

        :param token: API token for authentication.
        :param secret: API secret for authentication.
        :param domain_name: The target domain name to manage.
        :param record_type: The default DNS record type to use.
        :param base_url: The base URL for the Domeneshop API.
        """
        self.token = token
        self.secret = secret
        self.base_url = base_url
        self.domain_name = domain_name
        self.record_type = record_type
        self.headers = self._create_headers()
    
    def _create_headers(self):
        """
        Create the authorization headers for API requests.

        :return: A dictionary containing the necessary headers.
        """
        credentials = f"{self.token}:{self.secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def get_domains(self):
        """
        Retrieve the list of domains associated with the account.

        :return: A list of domains or None if an error occurs.
        """
        url = f"{self.base_url}/domains"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                print("Error: Response is not valid JSON.")
                return None
        else:
            print(f"Error fetching domains: {response.status_code} - {response.text}")
            return None
    
    def find_domain_id(self, domain_name=None):
        """
        Find the domain ID for a given domain name.

        :param domain_name: The domain name to search for. Defaults to the instance's domain_name.
        :return: The domain ID if found, else None.
        """
        domain_name = domain_name or self.domain_name
        domains = self.get_domains()
        if domains:
            for domain in domains:
                if domain.get('domain') == domain_name:
                    return domain.get('id')
        print(f"Domain '{domain_name}' not found.")
        return None
    
    def get_dns_records(self, domain_id):
        """
        Retrieve DNS records for a specific domain.

        :param domain_id: The ID of the domain.
        :return: A list of DNS records or None if an error occurs.
        """
        url = f"{self.base_url}/domains/{domain_id}/dns"
        response = requests.get(url, headers=self.headers)
        self._print_debug_info(response)
        
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                print("Error: Response is not valid JSON.")
                return None
        else:
            print(f"Error fetching DNS records: {response.status_code} - {response.text}")
            return None
    
    def add_dns_record(self, domain_id, host, record_type, data, ttl=3600):
        """
        Add a new DNS record to a domain.

        :param domain_id: The ID of the domain.
        :param host: The host/subdomain for the DNS record.
        :param record_type: The type of DNS record (e.g., 'A', 'CNAME').
        :param data: The data for the DNS record (e.g., IP address).
        :param ttl: Time to live for the DNS record.
        :return: The newly created DNS record or None if an error occurs.
        """
        url = f"{self.base_url}/domains/{domain_id}/dns"
        payload = {
            "host": host,
            "ttl": ttl,
            "type": record_type,
            "data": data
        }
        response = requests.post(url, headers=self.headers, json=payload)
        self._print_debug_info(response)
        
        if response.status_code == 201:
            print(f"DNS record added: {host}.{self.domain_name}")
            return response.json()
        else:
            print(f"Error adding DNS record: {response.status_code} - {response.text}")
            return None
    
    def update_dns_record(self, domain_id, record_id, host, record_type, data, ttl=3600):
        """
        Update an existing DNS record.

        :param domain_id: The ID of the domain.
        :param record_id: The ID of the DNS record to update.
        :param host: The host/subdomain for the DNS record.
        :param record_type: The type of DNS record (e.g., 'A', 'CNAME').
        :param data: The new data for the DNS record.
        :param ttl: Time to live for the DNS record.
        :return: The updated DNS record or None if an error occurs.
        """
        url = f"{self.base_url}/domains/{domain_id}/dns/{record_id}"
        payload = {
            "host": host,
            "ttl": ttl,
            "type": record_type,
            "data": data
        }
        response = requests.put(url, headers=self.headers, json=payload)
        self._print_debug_info(response)
        
        if response.status_code == 200:
            print(f"DNS record updated: {host}.{self.domain_name}")
            return response.json()
        else:
            print(f"Error updating DNS record: {response.status_code} - {response.text}")
            return None
    
    def delete_dns_record(self, domain_id, record_id):
        """
        Delete a DNS record from a domain.

        :param domain_id: The ID of the domain.
        :param record_id: The ID of the DNS record to delete.
        """
        url = f"{self.base_url}/domains/{domain_id}/dns/{record_id}"
        response = requests.delete(url, headers=self.headers)
        self._print_debug_info(response)
        
        if response.status_code == 204:
            print(f"DNS record with ID {record_id} deleted.")
        else:
            print(f"Error deleting DNS record: {response.status_code} - {response.text}")
    
    def list_dns_records(self, domain_id, print_output=False):
        """
        List all DNS records for a domain.

        :param domain_id: The ID of the domain.
        :return: A list of DNS records or None if an error occurs.
        """
        dns_records = self.get_dns_records(domain_id)
        if dns_records:
            if print_output:
                print(f"\nDNS records for domain ID {domain_id}:")
                for record in dns_records:
                    print(f"Record ID: {record.get('id')}, Host: {record.get('host')}, "
                          f"Type: {record.get('type')}, Data: {record.get('data')}, "
                          f"TTL: {record.get('ttl', 'N/A')}")
            return dns_records
        return None
