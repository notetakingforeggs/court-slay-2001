# notes to self

## starting up
```bash
~/dev/court-slay-2001/scripts/setup_db.sh     # first time / fresh db only
docker compose -f docker-compose.dev.yaml up -d
```

## db
```bash
dbcon    # if not working: source ~/.zshrc first
```

## secrets
- bot token lives in `.env` (not committed) — get new one from @BotFather if needed
- courtserve creds in `court_scraper_service/.env.dev`
- never commit either of these

## docker pulls hanging
check `~/.docker/config.json` — remove `"credsStore": "desktop"` if it's back

## rebuild just the backend
```bash
docker compose -f docker-compose.dev.yaml up -d --build app
```
