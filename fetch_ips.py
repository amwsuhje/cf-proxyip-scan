import requests
import re

SOURCES = [
    'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz'
]

IP_PATTERN = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

def fetch_ips():
    ip_set = set()
    for url in SOURCES:
        try:
            resp = requests.get(url, timeout=10)
            matches = re.findall(IP_PATTERN, resp.text)
            ip_set.update(matches)
        except Exception as e:
            print(f"[!] Error fetching from {url}: {e}")
    return list(ip_set)
