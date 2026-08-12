"""FastF1-backed data layer for the APEX F1 website."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

import fastf1
import pandas as pd
import requests

logger = logging.getLogger(__name__)

CACHE_DIR = Path(__file__).resolve().parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR / "fastf1"))

JOLPICA_BASE = "https://api.jolpi.ca/ergast/f1"


def current_season() -> int:
    return datetime.now(timezone.utc).year


def _to_iso(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, pd.Timestamp):
        if pd.isna(value):
            return None
        return value.isoformat()
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def _fmt_timedelta(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        td = pd.to_timedelta(value)
    except (ValueError, TypeError):
        return None
    if pd.isna(td):
        return None
    total = td.total_seconds()
    if total < 0:
        return None
    hours = int(total // 3600)
    minutes = int((total % 3600) // 60)
    seconds = total % 60
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:06.3f}"
    return f"{minutes}:{seconds:06.3f}"


def _event_payload(row: pd.Series) -> dict[str, Any]:
    return {
        "round": int(row["RoundNumber"]),
        "name": str(row["EventName"]),
        "official_name": str(row.get("OfficialEventName") or row["EventName"]),
        "country": str(row["Country"]),
        "location": str(row["Location"]),
        "format": str(row.get("EventFormat") or "conventional"),
        "event_date": _to_iso(row.get("EventDate")),
        "race_date": _to_iso(row.get("Session5DateUtc") or row.get("Session5Date") or row.get("EventDate")),
        "sessions": {
            str(row.get(f"Session{i}") or f"Session{i}"): _to_iso(
                row.get(f"Session{i}DateUtc") or row.get(f"Session{i}Date")
            )
            for i in range(1, 6)
            if row.get(f"Session{i}")
        },
    }


@lru_cache(maxsize=4)
def get_schedule(year: int | None = None) -> list[dict[str, Any]]:
    year = year or current_season()
    now = datetime.now(timezone.utc)
    schedule = fastf1.get_event_schedule(year, include_testing=False)
    events: list[dict[str, Any]] = []
    for _, row in schedule.iterrows():
        if int(row["RoundNumber"]) <= 0:
            continue
        event = _event_payload(row)
        race_date = event.get("race_date")
        if race_date:
            when = datetime.fromisoformat(race_date)
            if when.tzinfo is None:
                when = when.replace(tzinfo=timezone.utc)
            event["status"] = "completed" if when < now else "upcoming"
        else:
            event["status"] = "unknown"
        events.append(event)
    return events


def get_next_race(year: int | None = None) -> dict[str, Any] | None:
    year = year or current_season()
    now = datetime.now(timezone.utc)
    for event in get_schedule(year):
        race_date = event.get("race_date")
        if not race_date:
            continue
        when = datetime.fromisoformat(race_date)
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        if when >= now:
            return {**event, "season": year, "status": "upcoming"}
    return None


def get_latest_completed_race(year: int | None = None) -> dict[str, Any] | None:
    year = year or current_season()
    now = datetime.now(timezone.utc)
    completed = []
    for event in get_schedule(year):
        race_date = event.get("race_date")
        if not race_date:
            continue
        when = datetime.fromisoformat(race_date)
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        if when < now:
            completed.append(event)
    return completed[-1] if completed else None


@lru_cache(maxsize=64)
def get_race_results(year: int, round_number: int) -> dict[str, Any]:
    session = fastf1.get_session(year, round_number, "R")
    session.load(laps=False, telemetry=False, weather=False, messages=False)

    results = []
    for _, row in session.results.sort_values("Position").iterrows():
        position = row.get("Position")
        if pd.isna(position):
            continue
        results.append(
            {
                "position": int(position),
                "driver_number": str(row.get("DriverNumber") or ""),
                "abbreviation": str(row.get("Abbreviation") or ""),
                "full_name": str(row.get("FullName") or ""),
                "team": str(row.get("TeamName") or ""),
                "team_color": f"#{row['TeamColor']}" if row.get("TeamColor") else None,
                "grid": int(row["GridPosition"]) if not pd.isna(row.get("GridPosition")) else None,
                "status": str(row.get("Status") or ""),
                "time": _fmt_timedelta(row.get("Time")),
                "points": float(row["Points"]) if not pd.isna(row.get("Points")) else 0.0,
                "laps": int(row["Laps"]) if not pd.isna(row.get("Laps")) else None,
                "headshot": row.get("HeadshotUrl") if isinstance(row.get("HeadshotUrl"), str) else None,
            }
        )

    event = session.event
    return {
        "season": year,
        "round": round_number,
        "name": str(event["EventName"]),
        "country": str(event["Country"]),
        "location": str(event["Location"]),
        "results": results,
    }


def get_driver_standings(year: int | None = None) -> list[dict[str, Any]]:
    year = year or current_season()
    url = f"{JOLPICA_BASE}/{year}/driverStandings.json"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        lists = response.json()["MRData"]["StandingsTable"]["StandingsLists"]
        if not lists:
            return []
        standings = []
        for entry in lists[0]["DriverStandings"]:
            driver = entry["Driver"]
            constructor = entry["Constructors"][0] if entry.get("Constructors") else {}
            standings.append(
                {
                    "position": int(entry["position"]),
                    "points": float(entry["points"]),
                    "wins": int(entry.get("wins") or 0),
                    "driver": f"{driver.get('givenName', '')} {driver.get('familyName', '')}".strip(),
                    "code": driver.get("code") or driver.get("familyName", "")[:3].upper(),
                    "nationality": driver.get("nationality"),
                    "team": constructor.get("name"),
                }
            )
        return standings
    except Exception as exc:  # noqa: BLE001
        logger.warning("Driver standings unavailable: %s", exc)
        return []


def get_constructor_standings(year: int | None = None) -> list[dict[str, Any]]:
    year = year or current_season()
    url = f"{JOLPICA_BASE}/{year}/constructorStandings.json"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        lists = response.json()["MRData"]["StandingsTable"]["StandingsLists"]
        if not lists:
            return []
        standings = []
        for entry in lists[0]["ConstructorStandings"]:
            constructor = entry["Constructor"]
            standings.append(
                {
                    "position": int(entry["position"]),
                    "points": float(entry["points"]),
                    "wins": int(entry.get("wins") or 0),
                    "team": constructor.get("name"),
                    "nationality": constructor.get("nationality"),
                }
            )
        return standings
    except Exception as exc:  # noqa: BLE001
        logger.warning("Constructor standings unavailable: %s", exc)
        return []


def get_season_snapshot(year: int | None = None) -> dict[str, Any]:
    year = year or current_season()
    schedule = get_schedule(year)
    next_race = get_next_race(year)
    latest = get_latest_completed_race(year)
    latest_results = None
    if latest:
        try:
            latest_results = get_race_results(year, latest["round"])
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not load latest results: %s", exc)

    return {
        "season": year,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "next_race": next_race,
        "latest_race": latest_results,
        "schedule": schedule,
        "driver_standings": get_driver_standings(year),
        "constructor_standings": get_constructor_standings(year),
    }
