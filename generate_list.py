from geoip import get_country

def write_proxy_list(ip_list):
    with open("proxyip.txt", "w") as f:
        for ip in sorted(ip_list):
            cc = get_country(ip)
            f.write(f"{cc} | {ip}\n")
