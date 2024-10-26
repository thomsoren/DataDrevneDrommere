import os
from dotenv import load_dotenv
from PiDomainHandler import PiDomainHandler

load_dotenv("config/.env")

TOKEN = os.getenv('TOKEN') 
SECRET = os.getenv('SECRET')
API_BASE_URL = "https://api.domeneshop.no/v0"

handler = PiDomainHandler(TOKEN, SECRET)

id = handler.find_domain_id("codexenmo.online")
records = handler.get_dns_records(id)
for record in records:
    print(record)
# handler.delete_dns_record(id, 6715346)
# handler.delete_dns_record(id, 6714616)

# handler.add_dns_record(id, "www", "A", "51.120.12.159")
# print(handler.list_dns_records(id))
