import requests
from bs4 import BeautifulSoup

url = "https://www.reddit.com/search/?q=The+Lost+Bus&type=posts&sort=hot&cId=b5d005a2-e354-4197-a58b-7ffe05681071&iId=f59184c4-8154-4a50-b896-92215b7cfd20"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "DNT": "1"  
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
post_links = []

for h2 in soup.find_all("h2", class_="m-0"):
    a_tag = h2.find("a", href=True)
    if a_tag and a_tag["href"].startswith("/r/"):
        post_links.append("https://www.reddit.com" + a_tag["href"])
    if len(post_links) >= 10:
        break

print(f"Found {len(post_links)} posts.")
print("-" * 80)

for index, post_url in enumerate(post_links, 1):
    json_url = post_url.rstrip("/") + ".json"
    print(f"\n[{index}] Fetching: {json_url}")

    try:
        res = requests.get(json_url, headers=headers)
        if res.status_code != 200:
            print(f"Failed ({res.status_code})")
            continue

        data = res.json()

        main_post = data[0]["data"]["children"][0]["data"]
        title = main_post.get("title", "No Title")
        main_comment = main_post.get("selftext", "")

        print(f"\nTitle: {title}")
        print(f"Main Comment (selftext):\n{main_comment[:400]}...\n")

        comments = data[1]["data"]["children"]
        for i, c in enumerate(comments[:10], 1):
            if "data" in c and "body" in c["data"]:
                print(f"SubComment {i}: {c['data']['body'][:250]}...\n")


    except Exception as e:
        print(f"Error parsing {post_url}: {e}")
        continue
