import requests

from scraper import stats
from scraper import scores
from scraper.schedule import get_schedule, print_schedule
from . import roster

players = roster.get_roster()
print("-----------------Roster:-----------------")
for player in players:
    print(player)

games = get_schedule()
print("-----------------Schedule:-----------------")
print_schedule(games)

playerStats = stats.get_stats()
print("-----------------Player Stats:-----------------")
stats.print_stats(playerStats)

scores1 = scores.get_scores()
print("-----------------Scores:-----------------")
scores.print_scores(scores1)
