import requests
import json
import re
from urllib.parse import unquote
from bs4 import BeautifulSoup
from config.settings import STATS_URL, AUTH_TICKET

headers = {
    "Authorization": AUTH_TICKET,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.langleyhockeyhouse.com",
    "Referer": "https://www.langleyhockeyhouse.com/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "Android",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
}


def get_stats() -> list[dict]:
    res = requests.get(STATS_URL, headers=headers)
    return parse_stats_response(res.json()["content"])

def parse_stats_response(raw_content: str) -> list[dict]:
    """
    Extracts and organizes player roster data from the DigitalShift HTML/Angular response.
    Returns a list of cleaned player dictionaries.
    """
    soup = BeautifulSoup(raw_content, "html.parser")
    
    players = []
    rows = soup.select_one("table").select("tbody tr")
    
    for row in rows:
        name_cell = row.select_one(".main-column-name a")
        if not name_cell:
            continue

        href = name_cell.get("href", "")
        player_id = href.split("/")[-1] if href else None

        number_span = row.select_one(".p")
        number = number_span.text.strip().lstrip("#") if number_span else None

        cols = row.find_all("td")
        stats = [td.text.strip() for td in cols]

        players.append({
            "player_id":  player_id,
            "name":       name_cell.text.strip(),
            "number":     number,
            "games_played": stats[3] if len(stats) > 3 else None,
            "goals":      stats[4] if len(stats) > 4 else None,
            "assists":    stats[5] if len(stats) > 5 else None,
            "points":     stats[6] if len(stats) > 6 else None,
            "penalty_minutes": stats[7] if len(stats) > 7 else None,
        })

    return players


def print_stats(players: list[dict]) -> None:
    for player in players:
        print(
            f"{player['name']} (#{player['number']}) - {player['position']} | Games Played: {player['games played']}, Goals: {player['goals']}, Assists: {player['assists']}, Points: {player['points']}, Penalty Minutes: {player['penalty minutes']}"
        )
