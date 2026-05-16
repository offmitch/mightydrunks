import requests
import json
import os
import time
import re
from urllib.parse import unquote
from config.settings import SCHEDULE_URL, AUTH_TICKET

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

CACHE_FILE = "schedule_cache.json"
CACHE_DURATION = 60 * 60 * 24 * 7

def get_schedule() -> list[dict]:
    # Check if cache exists and is still valid
    if os.path.exists(CACHE_FILE):
        file_age = time.time() - os.path.getmtime(CACHE_FILE)

        if file_age < CACHE_DURATION:
            with open(CACHE_FILE, "r") as f:
                print("Loading schedule from cache...")
                return json.load(f)

    # Otherwise fetch fresh data
    print("Fetching fresh schedule from API...")

    res = requests.get(SCHEDULE_URL, headers=headers)
    games = parse_schedule_response(res.json()["content"])

    # Save to cache
    with open(CACHE_FILE, "w") as f:
        json.dump(games, f, indent=2)

    return games

def parse_schedule_response(raw_content: str) -> list[dict]:

    match = re.search(r'ng-init="ctrl\.schedule=(\[.*?\])"', raw_content)
    if not match:
        raise ValueError("Could not find schedule data in response")

    json_str = match.group(1).replace('&quot;', '"')
    games_raw = json.loads(json_str)

    games = []
    for g in games_raw:
        games.append({
            "game_id":          g["game_id"],
            "status":           g["status"],
            "game_type":        g["game_type"],
            "date":             g["date"],
            "time":             g["time"],
            "datetime":         g["datetime"],
            "datetime_tz":      g["datetime_tz"],
            "time_zone":        g["time_zone"],
            "facility":         g["facility"],
            "facility_address": unquote(g["facility_address"]),
            "division":         g["home_division"],
            "home": {
                "team_id": g["home_team_id"],
                "team":    g["home_team"],
                "score":   g["home_score"],
                "shots":   g["home_shots"],
                "pim":     g["home_penalty_minutes"],
            },
            "away": {
                "team_id": g["away_team_id"],
                "team":    g["away_team"],
                "score":   g["away_score"],
                "shots":   g["away_shots"],
                "pim":     g["away_penalty_minutes"],
            },
            "overtime": g["overtime"],
            "shootout": g["shootout"],
        })

    return games


def print_schedule(games: list[dict]) -> None:
    for game in games:
        print(
            f"{game['date']} {game['time']}  |  "
            f"{game['home']['team']} vs {game['away']['team']}  |  "
            f"{game['facility']}  |  {game['status']}"
        )


if __name__ == "__main__":
    schedule = get_schedule()
    print_schedule(schedule)
    print(json.dumps(schedule, indent=2))