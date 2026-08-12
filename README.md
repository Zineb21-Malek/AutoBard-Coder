# APEX — Formula 1 race data

Flask site powered by **FastF1** for the season calendar, next race, and race classifications, plus championship standings from Jolpica.

## Features

- Next race hero with live countdown
- Latest race results (top 10 + full classification pages)
- Driver & constructor championship tables
- Full season calendar with links to each race
- JSON API endpoints under `/api/*`

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5050

Optional: `PORT=8080 python app.py`

## API

| Endpoint | Description |
|---|---|
| `GET /api/snapshot` | Season bundle (next race, latest results, schedule, standings) |
| `GET /api/schedule` | Event schedule |
| `GET /api/next-race` | Upcoming grand prix |
| `GET /api/race/<round>` | Race classification |
| `GET /api/standings/drivers` | Driver championship |
| `GET /api/standings/constructors` | Constructor championship |

Query `?season=YYYY` on pages and APIs to select a year.
