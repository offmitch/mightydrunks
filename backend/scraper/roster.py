import requests
from bs4 import BeautifulSoup

from config.settings import AUTH_TICKET
URL = "https://web.api.digitalshift.ca/partials/stats/team/stats?team_id=633828"

HEADERS = {
    "Authorization": AUTH_TICKET,
    "User-Agent": "Mozilla/5.0"
}

def get_roster():
    res = requests.get(URL, headers=HEADERS)
    data = res.json()

    if "content" not in data:
        print("ERROR:", data)
        return []

    soup = BeautifulSoup(data["content"], "html.parser")

    rows = soup.select(".table-scroll table tbody tr")

    players = []
    seen = set()

    for row in rows:
        cols = row.find_all("td")

        if len(cols) < 3:
            continue

        number = cols[0].text.strip() or None

        name_tag = cols[1].find("a")
        name = name_tag.text.strip() if name_tag else cols[1].text.strip()

        position = cols[2].text.strip()
        
        key = (name, number, position)

        if key in seen:
            continue

        seen.add(key)

        players.append({
            "number": number,
            "name": name,
            "position": position
        })

    return players