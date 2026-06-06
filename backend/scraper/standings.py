import requests
import os
from bs4 import BeautifulSoup
import re
import json
from scraper.schedule import CACHE_FILE, should_refresh_cache
from config.settings import SCORES_URL, STANDINGS_URL, AUTH_TICKET

HEADERS = {
    "Authorization": AUTH_TICKET,
    "Origin": "https://www.langleyhockeyhouse.com",
    "Referer": "https://www.langleyhockeyhouse.com/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36",
}

CACHE_FILE = "standings_cache.json"


def get_standings(schedule: list[dict]) -> list[dict]:

    if not should_refresh_cache(schedule):
        with open(CACHE_FILE, "r") as f:
            print("Loading standings from cache...")
            return json.load(f)

    standings = fetch_standings()

    with open(CACHE_FILE, "w") as f:
        json.dump(standings, f, indent=2)

    return standings

def fetch_standings() -> list[dict]:

    print("Fetching fresh standings from API...")

    res = requests.get(STANDINGS_URL, headers=HEADERS)
    res.raise_for_status()

    return parse_standings_response(res.json()["content"])

def refresh_standings_cache() -> list[dict]:

    standings = fetch_standings()

    with open(CACHE_FILE, "w") as f:
        json.dump(standings, f, indent=2)

    return standings    

def parse_standings_response(raw_content: str) -> list[dict]:
    soup = BeautifulSoup(raw_content, "html.parser")

    standings = []

    # First standings table only (avoids duplicate fixed table)
    table = soup.select_one("table.stats-table.standings")
    if not table:
        raise ValueError("Could not find standings table")

    rows = table.select("tbody tr")

    for row in rows:
        cols = row.find_all("td")

        team_link = row.select_one("a.team-inline")

        team_id = None
        if team_link:
            match = re.search(r"/team/(\d+)", team_link["href"])
            if match:
                team_id = int(match.group(1))

        standings.append({
            "rank": int(cols[0].get_text(strip=True)),
            "team": {
                "team_id": team_id,
                "name": team_link.get_text(strip=True) if team_link else None,
            },
            "gp": int(cols[2].get_text(strip=True)),
            "wins": int(cols[3].get_text(strip=True)),
            "losses": int(cols[4].get_text(strip=True)),
            "ties": int(cols[5].get_text(strip=True)),
            "ot_wins": int(cols[6].get_text(strip=True)),
            "ot_losses": int(cols[7].get_text(strip=True)),
            "points": int(cols[8].get_text(strip=True)),
            "win_pct": float(cols[9].get_text(strip=True)),
            "regulation_wins": int(cols[10].get_text(strip=True)),
            "goals_for": int(cols[11].get_text(strip=True)),
            "goals_against": int(cols[12].get_text(strip=True)),
            "goal_diff": cols[13].get_text(strip=True),
            "pim": int(cols[14].get_text(strip=True)),
            "last_10": cols[15].get_text(" ", strip=True),
            "streak": cols[16].get_text(strip=True),
        })

    return standings

def print_standings(standings: list[dict]):
    for standing in standings:
        print(f"{standing['rank']}. {standing['team']['name']} - GP: {standing['gp']}, W: {standing['wins']}, L: {standing['losses']}, T: {standing['ties']}")