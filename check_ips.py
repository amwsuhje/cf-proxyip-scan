import asyncio
import aiohttp

WORKER_HOST = "winnie.winniezhang.workers.dev"

async def is_cf_proxy(ip):
    url = f"http://{ip}"
    headers = {
        "Host": WORKER_HOST,
        "User-Agent": "Mozilla/5.0"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=6) as resp:
                if resp.status == 200:
                    print(f"[✓] {ip} 可访问 Workers")
                    return True
    except Exception as e:
        pass
    return False

async def check_ips(ip_list):
    print("[*] 正在检测 IP 可用性...")
    tasks = [is_cf_proxy(ip) for ip in ip_list]
    results = await asyncio.gather(*tasks)
    return [ip for ip, ok in zip(ip_list, results) if ok]
