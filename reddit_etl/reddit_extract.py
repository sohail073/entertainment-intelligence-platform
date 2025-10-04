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
    
    # Find all <h2> tags containing post titles
    post_titles = soup.find_all("h2", class_="m-0")
    
    # Extract the href from the <a> tag inside <h2>, limit to 10
    for i, h2 in enumerate(post_titles[:10], 1):
        a_tag = h2.find("a", href=True)
        if a_tag:
            print(f"{i}: https://www.reddit.com{a_tag['href']}")
else:
    print(f"Error {response.status_code}")
