# APEX — Formula 1 race data

Flask site powered by **FastF1** for the season calendar, next race, and race classifications, plus championship standings from Jolpica.

## Features

- Next race hero with live countdown
- Latest race results (top 10 + full classification pages)
- Driver & constructor championship tables
- Full season calendar with links to each race
- JSON API endpoints under `/api/*`

## Setup (local)

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5050

Optional: `PORT=8080 python app.py`

## Free online view (Render)

GitHub Pages cannot host this Flask app. Use **Render** (free):

1. Go to https://render.com and sign in with GitHub
2. **New** → **Web Service** → select this repository / branch
3. Settings (usually auto-filled from `render.yaml`):
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`
4. Create the service → open the `*.onrender.com` URL

First load can take ~30–60s on the free tier (cold start).

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
