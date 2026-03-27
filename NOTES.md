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

---

## routine maintenance checklist

### weekly
- [ ] **scraper running?**
  ```bash
  docker ps --format "{{.Names}}\t{{.Status}}" | grep scraper
  ```
  should say `Up X hours/days`. if exited: `dc up -d scraper`

- [ ] **scrapes happening?** check for the `===` banners in scraper logs
  ```bash
  docker logs court-slay-2001-scraper-1 --since 48h 2>&1 | grep "SCRAPE"
  ```
  expect one `STARTING` + one `COMPLETE` per day (runs at 01:00)

- [ ] **new cases being added?** look for non-zero new counts
  ```bash
  docker logs court-slay-2001-scraper-1 --since 48h 2>&1 | grep "COMPLETE"
  ```

- [ ] **backup ran?**
  ```bash
  tail -20 ~/dev/court-slay-2001/logs/backup.log
  ```
  expect a `Backup written` line each day (runs at 03:00)

- [ ] **backup files present on HDD?**
  ```bash
  ls -lh /Volumes/ExternalHDD/court-slay-backups/
  ```

### monthly
  ```bash
  docker logs court-slay-2001-scraper-1 --since 7d 2>&1 | grep "ERROR" | sort | uniq -c | sort -rn | head -20
  ```
