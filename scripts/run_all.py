from scraper.schedule import get_schedule
from database.insert import insert_games

def run():
    games = get_schedule()
    insert_games(games)
    print("Schedule updated!")

if __name__ == "__main__":
    run()