from flask import Flask, jsonify
from flask_cors import CORS
from scraper.scores import get_scores
from scraper.schedule import get_schedule
from scraper.roster import get_roster
from scraper.stats import get_stats

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

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
        players = get_stats()
        return jsonify(players)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/schedule")
def schedule():
    try:
        games = get_schedule()
        return jsonify(games)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/scores")
def scores():
    try:
        scores = get_scores()
        return jsonify(scores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)