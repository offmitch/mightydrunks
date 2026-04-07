import requests
from bs4 import BeautifulSoup
from config.settings import SCHEDULE_URL

headers = {
    "Authorization": 'ticket="rQd80er06_iK2XNXtVrztisEL_oda-P-_-97NNgY1z0RrH_30sDUVi9jh5JKuueOBpKpHCIyP7X9spkHdj6GTtk2"',
    "User-Agent": "Mozilla/5.0"
}

def get_schedule():
    url = SCHEDULE_URL
    res = requests.get(url, headers=headers)
    data = res.json()

    
    html = data["content"]
    soup = BeautifulSoup(html, "html.parser")

    games = []

    rows = soup.select("table tbody tr")

    for row in rows:
        cols = row.find_all("td")

        if len(cols) < 3:
            continue

        number = cols[0].text.strip()
        number = number if number else None
        name = cols[1].text.strip()
        position = cols[2].text.strip()

        players.append({
            "number": number,
            "name": name,
            "position": position
        })

    return players

