import asyncio
import aiohttp

async def is_cf_proxy(ip):
    test_url = f"http://{ip}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(test_url, timeout=5) as resp:
                return resp.status in [200, 403]
    except:
        return False

async def check_ips(ip_list):
    tasks = [is_cf_proxy(ip) for ip in ip_list]
    results = await asyncio.gather(*tasks)
    return [ip for ip, ok in zip(ip_list, results) if ok]
