import requests
import json
from bs4 import BeautifulSoup

url = "https://web.api.digitalshift.ca/partials/stats/team/roster?team_id=633828"

headers = {
    "Accept": "application/json",
    "Authorization": 'ticket="rQd80er06_iK2XNXtVrztisEL_oda-P-_-97NNgY1z0RrH_30sDUVi9jh5JKuueOBpKpHCIyP7X9spkHdj6GTtk2"',
    "Origin": "https://www.langleyhockeyhouse.com",
    "Referer": "https://www.langleyhockeyhouse.com/",
    "User-Agent": "Mozilla/5.0"
}


res = requests.get(url, headers=headers)
data = res.json()

html = data["content"]

# Parse the HTML inside the JSON
soup = BeautifulSoup(html, "html.parser")

# print(soup.prettify()[:1000])  

players = []

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

for p in players:
    print(p)