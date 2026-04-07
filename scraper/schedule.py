import requests
from bs4 import BeautifulSoup

def get_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    return BeautifulSoup(res.text, "html.parser")

def scrape_schedule(url):
    soup = get_page(url)

    games = []

    rows = soup.select("table tr")  # adjust selector

    for row in rows[1:]:  # skip header
        cols = row.find_all("td")

        if len(cols) == 0:
            continue

        game = {
            "date": cols[0].text.strip(),
            "home": cols[1].text.strip(),
            "away": cols[2].text.strip(),
            "score": cols[3].text.strip()
        }

        games.append(game)

    return games