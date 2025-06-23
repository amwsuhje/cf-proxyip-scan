import requests

def get_country(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=5)
        if r.status_code == 200:
            return r.json().get("countryCode", "??")
    except:
        pass
    return "??"
