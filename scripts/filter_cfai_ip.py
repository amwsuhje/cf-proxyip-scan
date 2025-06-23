import aiohttp
import asyncio

INPUT_FILE = "proxyip.txt"
OUTPUT_FILE = "CFAIip.txt"
TEST_URLS = [
    "https://chat.openai.com",
    "https://cloudflare.com"
]

TIMEOUT = aiohttp.ClientTimeout(total=8)

async def test_ip(ip, urls):
    proxy = f"http://{ip}"  # 依赖 Cloudflare IP 支持 HTTP 代理
    try:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            for url in urls:
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
        print(f"Testing region: {region}, total IPs: {len(ip_list)}")
        tasks = [test_ip(ip, TEST_URLS) for ip in ip_list]
        results = await asyncio.gather(*tasks)
        valid_ips = [ip for ip, ok in zip(ip_list, results) if ok]
        if valid_ips:
            filtered_result[region] = valid_ips
            print(f"✅ Region {region} passed: {len(valid_ips)} IPs")
        else:
            print(f"❌ Region {region} has no valid IPs")

    with open(OUTPUT_FILE, "w") as f:
        for region, ip_list in filtered_result.items():
            f.write(region + "\n")
            for ip in ip_list:
                f.write(ip + "\n")
            f.write("\n")

if __name__ == "__main__":
    asyncio.run(filter_ips())
