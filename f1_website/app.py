"""APEX — Formula 1 race data website powered by FastF1."""

from __future__ import annotations

import logging
import os

from flask import Flask, jsonify, render_template, request

from f1_data import (
    current_season,
    get_constructor_standings,
    get_driver_standings,
    get_next_race,
    get_race_results,
    get_schedule,
    get_season_snapshot,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    season = request.args.get("season", type=int) or current_season()
    snapshot = get_season_snapshot(season)
    return render_template("index.html", snapshot=snapshot)


@app.route("/race/<int:round_number>")
def race_detail(round_number: int):
    season = request.args.get("season", type=int) or current_season()
    try:
        results = get_race_results(season, round_number)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to load race %s", round_number)
        return render_template(
            "race.html",
            error=str(exc),
            season=season,
            round_number=round_number,
            results=None,
        ), 404
    return render_template("race.html", results=results, error=None, season=season)


@app.route("/api/snapshot")
def api_snapshot():
    season = request.args.get("season", type=int) or current_season()
    return jsonify(get_season_snapshot(season))


@app.route("/api/schedule")
def api_schedule():
    season = request.args.get("season", type=int) or current_season()
    return jsonify({"season": season, "events": get_schedule(season)})


@app.route("/api/next-race")
def api_next_race():
    season = request.args.get("season", type=int) or current_season()
    return jsonify({"season": season, "next_race": get_next_race(season)})


@app.route("/api/race/<int:round_number>")
def api_race(round_number: int):
    season = request.args.get("season", type=int) or current_season()
    try:
        return jsonify(get_race_results(season, round_number))
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 404


@app.route("/api/standings/drivers")
def api_driver_standings():
    season = request.args.get("season", type=int) or current_season()
    return jsonify({"season": season, "standings": get_driver_standings(season)})


@app.route("/api/standings/constructors")
def api_constructor_standings():
    season = request.args.get("season", type=int) or current_season()
    return jsonify({"season": season, "standings": get_constructor_standings(season)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5050"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
