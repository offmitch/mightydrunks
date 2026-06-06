import os
from flask import Flask, jsonify
from flask_cors import CORS
from scraper.standings import get_standings
from scraper.scores import get_scores, refresh_scores_cache
from scraper.schedule import get_schedule
from scraper.roster import get_roster
from scraper.stats import get_stats, refresh_stats_cache

app = Flask(__name__)
CORS(app, origins=["https://mightydrunks.onrender.com"])
# CORS(app, origins=["http://localhost:3000"])


@app.route("/api/roster")
def roster():
    try:
        players = get_roster()
        return jsonify(players)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/stats")
def stats():
    try:
        schedule = get_schedule()
        players = get_stats(schedule)
        return jsonify(players)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route("/api/schedule")
def schedule_route():
    try:
        games = get_schedule()
        return jsonify(games)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/scores")
def scores():
    try:
        schedule = get_schedule()
        scores = get_scores(schedule)
        return jsonify(scores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/standings")
def standings():
    try:
        schedule = get_schedule()
        standings = get_standings(schedule)
        return jsonify(standings)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/refresh")
def refresh():
    stats = refresh_stats_cache()
    scores = refresh_scores_cache()

    return jsonify({
        "success": True,
        "stats_count": len(stats),
        "scores_count": len(scores)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    # app.run(debug=True)