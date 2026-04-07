import requests
from . import roster

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# def fetch_json(url):
#     res = requests.get(url, headers=HEADERS)
#     res.raise_for_status()
#     return res.json()

players = roster.get_roster()
for player in players:
    print(player)