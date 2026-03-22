# court-slay-2001

Scrapes UK civil court daily cause lists from CourtServe and alerts users via Telegram when hearings matching their subscribed names appear. Built for a legal advice service to help people find out about upcoming possession/eviction hearings.

---

## Architecture

| Component | Tech | What it does |
|---|---|---|
| `court_scraper_service/` | Python | Scrapes CourtServe daily, parses HTML, writes to DB |
| `backend/` | FastAPI | REST API + Telegram bot + daily notifier |
| `db/` | PostgreSQL | Stores court cases, subscriptions, reference data |

---

## First time setup

### Prerequisites
- Colima running with external drive mounted
- `.env` file in project root with `BOT_TOKEN`

### Start Colima
```bash
colima start --mount /Volumes/ExternalHDD:w
```

### Environment files
Two env files are needed and are **not committed to git**:

**`.env`** (project root) — for Docker Compose:
```
BOT_TOKEN=your_telegram_bot_token
```

**`court_scraper_service/.env.dev`** — for the scraper:
```
COURT_USERNAME=your_courtserve_email
COURT_PASSWORD=your_courtserve_password
DB_NAME=courtdb_dev
DB_USER=jonah
DB_PASS=jonah
DB_HOST=court_db_dev
DB_PORT=5432
```

### Fresh database setup
Run this once on a new machine or after wiping the DB:
```bash
~/dev/court-slay-2001/scripts/setup_db.sh
```

This will:
1. Start postgres
2. Create all tables
3. Seed regions (7) and courts (136)
4. Start all remaining services

---

## Day to day

### Start everything
```bash
cd ~/dev/court-slay-2001
docker compose -f docker-compose.dev.yaml up -d
```

### Stop everything
```bash
docker compose -f docker-compose.dev.yaml down
```

### Restart just the backend (after code changes)
```bash
docker compose -f docker-compose.dev.yaml up -d --build app
```

### View logs
```bash
docker compose -f docker-compose.dev.yaml logs -f
# or just one service:
docker compose -f docker-compose.dev.yaml logs -f scraper
docker compose -f docker-compose.dev.yaml logs -f app
```

---

## Database

### tmux panels

**Left — DB:**

```bash
# connect
dbcon
# (if not working: source ~/.zshrc first)

# set display options once connected
\pset pager always
\pset format wrapped

# main view — all cases with court name
SELECT * FROM court_case JOIN court ON court_case.court_id = court.id ORDER BY court.id;

-- search by claimant
SELECT * FROM court_case JOIN court ON court_case.court_id = court.id WHERE claimant ILIKE '%some text%';
```

**Right top — logs:**
```bash
docker compose -f docker-compose.dev.yaml logs -f
```

**Right bottom — working dir:**
```bash
cd ~/dev/court-slay-2001
```

-- count
SELECT COUNT(*) FROM court_case;

-- active subscriptions
SELECT * FROM subscription;
```

---

## Telegram bot

Bot token is stored in `.env` (never commit this). Get a new token via `@BotFather` on Telegram if needed.

### Commands
| Command | What it does |
|---|---|
| `/claimant: <name>` | Subscribe to alerts for a claimant name |
| `/defendant: <name>` | Subscribe to alerts for a defendant name |
| `/view` | See your current subscriptions |
| `/clear` | Remove your subscriptions |

---

## Scheduling

| Job | Time | Where |
|---|---|---|
| Scraper | 01:00 daily | `court_scraper_service/court_scraper/main.py` |
| Telegram notifier | 07:30 daily | `backend/notifier.py` |

Scraper also runs once immediately on container startup.

---

## Logging

Log levels are set to `INFO` by default. To get more detail change `level=logging.INFO` to `level=logging.DEBUG` in:
- `court_scraper_service/court_scraper/main.py`
- `backend/main.py`

Normal INFO output shows: scrape start/complete, per-court case counts, Telegram interactions.

---

## Networking

The server is accessed via Tailscale. Do not take Tailscale down while SSH'd in or you will lose your session.

Docker image pulls were previously broken due to `"credsStore": "desktop"` in `~/.docker/config.json` — this was removed. If pulls start hanging again, check that file.

---

## Ports

| Service | Port |
|---|---|
| FastAPI backend | 8000 |
| Nextcloud | 8080 |
| PostgreSQL (court) | 5433 |
