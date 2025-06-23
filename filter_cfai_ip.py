import asyncio
import aiohttp

INPUT_FILE = "proxyip.txt"
OUTPUT_FILE = "CFAIip.txt"
TEST_URLS = [
    "https://chat.openai.com",
    "https://cloudflare.com"
]
TIMEOUT = aiohttp.ClientTimeout(total=8)


async def test_ip(ip):
    proxy = f"http://{ip}"
    try:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            for url in TEST_URLS:
                async with session.get(url, proxy=proxy, ssl=False) as resp:
                    if resp.status != 200:
                        return False
        return True
    except:
        return False


async def filter_ips():
    region = None
    region_ips = {}
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if '.' not in line:
                region = line
                region_ips[region] = []
            else:
                region_ips[region].append(line)

    filtered_result = {}

    for region, ip_list in region_ips.items():
        print(f"[{region}] Testing {len(ip_list)} IPs...")
        tasks = [test_ip(ip) for ip in ip_list]
        results = await asyncio.gather(*tasks)
        valid_ips = [ip for ip, ok in zip(ip_list, results) if ok]
        if valid_ips:
            filtered_result[region] = valid_ips
            print(f"[{region}] ✅ {len(valid_ips)} passed.")
        else:
            print(f"[{region}] ❌ None passed.")

    with open(OUTPUT_FILE, "w") as f:
        for region, ips in filtered_result.items():
            f.write(region + "\n")
            for ip in ips:
                f.write(ip + "\n")
            f.write("\n")


if __name__ == "__main__":
    asyncio.run(filter_ips())
