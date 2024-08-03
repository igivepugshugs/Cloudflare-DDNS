# CloudFlare DDNS
Uses the Cloudflare API to automatically update a DNS record for a given domain. This tool works by running the container on a system inside of your network. While running, it will periodically check and update the CloudFlare DNS for a specified record.

Requires a CloudFlare account to work.

## What it does
1. Check LAN public IP every 5 minutes
2. Update Cloudflare once a change is noticed.
	- delete old record
	- create new record

## Get started
This guide requires docker be installed on your system. Alternatively, you can just use a python virtual environment.

1. Place root folder on a system inside of your LAN you wish to point external DNS to.
2. Create a '.env' file in the root directory.
3. paste the contents below into the .env file and add your relevant variables. Save the file.

	```
	# Your API key only needs the Edit DNS template for this to work. 

	# Your CloudFlare API key
	API_KEY=<YOUR_API_KEY>
	
	# Only needed if using Global API Key
	EMAIL=<YOUR_CLOUDFLARE_EMAIL>
	
	# Find this in your Cloudflare dashboard
	ZONE_ID=<YOUR_ZONE_ID>
	
	# Your domain name
	DOMAIN=<YOUR_DOMAIN>
	```

4. Build the docker container 

	```docker build -t ddns .```

5. Run the container and inject the .env into it. You may need to change the port if in use already.

	```docker run --env-file .env -d --name ddns -p 8080:80 ddns:latest```

6. Server is now running and you should see the root record for your specified domain is pointing at your LAN's public IP

## Customization
You can also change the type of record and the values associated by editing the below information found on line 50 of 'app.py' Read the comment on each line for usage details.
```
  # Data for the new DNS record
    data = {
        'type': 'A',  # Change to the type of DNS record you need (e.g., A, CNAME, TXT)
        'name': '@',  # Replace with the subdomain or root (@)
        'content': external_ip,  # Replace with the IP address or target of the DNS record
        'ttl': 120,  # Time to live (in seconds)
        'proxied': False  # Set to True if you want Cloudflare to proxy this record
    }
```
