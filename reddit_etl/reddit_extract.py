import requests
from bs4 import BeautifulSoup

# url = "https://www.reddit.com/search/?q=The+Lost+Bus&type=posts&sort=hot&cId=b5d005a2-e354-4197-a58b-7ffe05681071&iId=f59184c4-8154-4a50-b896-92215b7cfd20"

HEADERS = {
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

BASE_URL = "https://www.reddit.com"

def fetch_html(url):
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        raise Exception(f"Failed to load HTML ({res.status_code})")
    return res.text

def extract_post_links(html, limit=10):
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for h2 in soup.find_all("h2", class_="m-0"):
        a = h2.find("a", href=True)
        if a and a["href"].startswith("/r/"):
            links.append(BASE_URL + a["href"])
        if len(links) >= limit:
            break

    return links

def fetch_post_json(post_url):
    json_url = post_url.rstrip("/") + ".json"
    res = requests.get(json_url, headers=HEADERS)

    if res.status_code != 200:
        raise Exception(f"Failed JSON ({res.status_code})")

    return res.json()

def parse_post_data(data):
    main = data[0]["data"]["children"][0]["data"]

    title = main.get("title", "No Title")
    body = main.get("selftext", "")

    comments_raw = data[1]["data"]["children"]
    comments = [
        c["data"]["body"] for c in comments_raw
        if "data" in c and "body" in c["data"]
    ]

    return title, body, comments

def main():
    search_url = "https://www.reddit.com/search/?q=The+Lost+Bus&type=posts&sort=hot"

    print("Fetching search results...")
    html = fetch_html(search_url)

    post_links = extract_post_links(html)
    print(f"Found {len(post_links)} posts.")

    for idx, post_url in enumerate(post_links, 1):
        print("\n" + "-" * 70)
        print(f"[{idx}] {post_url}")

        try:
            data = fetch_post_json(post_url)
            title, body, comments = parse_post_data(data)

            print(f"\nTitle: {title}")
            print(f"Main Post:\n{body[:400]}...\n")

            for i, c in enumerate(comments[:10], 1):
                print(f"Comment {i}: {c[:250]}...\n")

        except Exception as e:
            print(f"Error: {e}")
            
if __name__ == "__main__":
    main()
    