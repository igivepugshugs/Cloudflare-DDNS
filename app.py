"""
app.py

REQUIREMENTS: 
- Cloudflare account with a domain for DNS lookups
- Cloudflare API key

DESCRIPTION
This app runs in a docker container and automatically updates Cloudflare DDNS
whenever it detects that LAN router's public IP has changed.

Don't forget to create a '.env' file in this directory. Check out the README for an example.
"""
import os
import json, time, requests
import urllib.request
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
email = os.getenv('EMAIL')  # Only needed if using Global API Key
zone_id = os.getenv('ZONE_ID') # Find this in your Cloudflare dashboard
domain = os.getenv('DOMAIN')  # Your domain name

print(api_key)
print(email)
print(zone_id)
print(domain)



RUNNING = True

while RUNNING:

    # Get the LAN external IP
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

    print("Your external ip address:" + external_ip)

    # Cloudflare API endpoint to create DNS records
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'

    headers = {
        'Authorization': f'Bearer {api_key}',  # Use 'X-Auth-Email' and 'X-Auth-Key' headers for Global API Key
        'Content-Type': 'application/json'
    }

    # Data for the new DNS record
    data = {
        'type': 'A',  # Change to the type of DNS record you need (e.g., A, CNAME, TXT)
        'name': '@',  # Replace with the subdomain or root (@)
        'content': external_ip,  # Replace with the IP address or target of the DNS record
        'ttl': 120,  # Time to live (in seconds)
        'proxied': False  # Set to True if you want Cloudflare to proxy this record
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("DNS record created successfully.")
        print(response.json())
    else:
        print(f"Failed to create DNS record. Status code: {response.status_code}, Error: {response.json()}")

    # Wait for 5 minutes, then check again.
    time.sleep(300)

