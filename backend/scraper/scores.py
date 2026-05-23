import requests
import re
import json
import os
import time
from urllib.parse import unquote
from backend.scraper.schedule import should_refresh_cache
from config.settings import SCORES_URL, AUTH_TICKET

HEADERS = {
    "Authorization": AUTH_TICKET,
    "Origin": "https://www.langleyhockeyhouse.com",
    "Referer": "https://www.langleyhockeyhouse.com/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36",
}

CACHE_FILE = "scores_cache.json"


def get_scores(schedule: list[dict]) -> list[dict]:

    # if not should_refresh_cache(schedule):
    #     with open(CACHE_FILE, "r") as f:
    #         print("Loading scores from cache...")
    #         return json.load(f)

    # Otherwise fetch fresh data
    print("Fetching fresh scores from API...")

    res = requests.get(SCORES_URL, headers=HEADERS)
    res.raise_for_status()
    scores = parse_scores_response(res.json()["content"])

    # Save to cache
    with open(CACHE_FILE, "w") as f:
        json.dump(scores, f, indent=2)

    return scores


def parse_scores_response(raw_content: str) -> list[dict]:
    match = re.search(r'ng-init="ctrl\.scores=(\[.*?\])"', raw_content)
    if not match:
        raise ValueError("Could not find scores data in response")

    json_str = match.group(1).replace('&quot;', '"')
    scores_raw = json.loads(json_str)

    scores = []
    for g in scores_raw:
        scores.append({
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

    return scores

def print_scores(scores: list[dict]):
    for score in scores:
        print(f"{score['date']} {score['time']} - {score['home']['team']} {score['home']['score']} vs {score['away']['team']} {score['away']['score']} ({score['status']})")
        