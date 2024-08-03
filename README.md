# LAN DDNS Server
Uses a Cloudflare API to automatically update the IP address of a DNS record
for a given domain.

## How it works
1. Check LAN public IP every 5 minutes
4. Save found IP locally for caching
5. Store IP in database with time of change, IP address, other trackable data if wanted
6. Update Cloudflare once a change is noticed.
	- delete old record
	- create new record

## Get started
Ill create a better way to start this, but for now just run the following:

docker build -t ddns .
docker run -d --name ddns -p 8080:80 ddns:latest