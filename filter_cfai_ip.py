import asyncio
import aiohttp
import time

INPUT_FILE = "proxyip.txt"
OUTPUT_FILE = "CFAIip.txt"
TEST_URLS = {
    "chatgpt": "https://chat.openai.com/favicon.ico",
    "cloudflare": "https://cloudflare.com"
}
MIN_SPEED = 1_000_000  # 1MB/s in Bytes
TIMEOUT = aiohttp.ClientTimeout(total=10)

async def test_ip(ip):
    proxy = f"http://{ip}"
    try:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            # 测试 cloudflare.com 可达性
            async with session.get(TEST_URLS["cloudflare"], proxy=proxy, ssl=False) as resp:
                if resp.status != 200:
                    return False

            # 测试 chat.openai.com 速度
            start = time.time()
            async with session.get(TEST_URLS["chatgpt"], proxy=proxy, ssl=False) as resp:
                if resp.status != 200:
                    return False
                content = await resp.read()
                duration = time.time() - start
                size = len(content)
                speed = size / duration  # Bytes per second
                if speed < MIN_SPEED:
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
