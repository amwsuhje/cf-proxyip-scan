from fetch_ips import fetch_ips
from check_ips import check_ips
from generate_list import write_proxy_list
import asyncio

if __name__ == "__main__":
    print("[+] Fetching IPs...")
    raw_ips = fetch_ips()
    print(f"[+] Got {len(raw_ips)} raw IPs")

    print("[+] Checking availability...")
    ok_ips = asyncio.run(check_ips(raw_ips))
    print(f"[+] {len(ok_ips)} usable IPs")

    print("[+] Writing proxyip.txt...")
    write_proxy_list(ok_ips)
    print("[✓] Done.")
