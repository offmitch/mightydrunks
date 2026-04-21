from dotenv import load_dotenv
import os

load_dotenv()

TEAM_ID = "633828"
AUTH_TICKET = os.getenv("AUTH_TICKET")

SCHEDULE_URL = f"https://web.api.digitalshift.ca/partials/stats/schedule/table?team_id={TEAM_ID}&header=false"
STATS_URL = f"https://web.api.digitalshift.ca/partials/stats/team/stats?team_id={TEAM_ID}"
ROSTER_URL = f"https://web.api.digitalshift.ca/partials/stats/team/roster?team_id={TEAM_ID}"
SCORES_URL = f"https://web.api.digitalshift.ca/partials/stats/scores/table?order=datetime&team_id={TEAM_ID}&offset=1&limit=20&header=false"
STANDINGS_URL = "https://www.langleyhockeyhouse.com/stats#/5/standings?render=division&division_id=48556"