from flask import Flask, jsonify
from flask_cors import CORS
from scraper.roster import get_roster

app = Flask(__name__)
CORS(app, origins=["http://localhost:8000"])

@app.route("/api/roster")
def roster():
    try:
        players = get_roster()
        return jsonify(players)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)