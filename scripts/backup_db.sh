#!/bin/bash
set -euo pipefail

BACKUP_DIR="/Volumes/ExternalHDD/court-slay-backups"
LOG_FILE="/Users/sqpk/dev/court-slay-2001/logs/backup.log"
DATE=$(date +%Y-%m-%d)
FILENAME="courtdb_${DATE}.sql.gz"
KEEP_DAYS=14

mkdir -p "$(dirname "$LOG_FILE")"
exec >> "$LOG_FILE" 2>&1

# Check external HDD is mounted
if [ ! -d "/Volumes/ExternalHDD" ]; then
    echo "[$(date)] ERROR: External HDD not mounted. Backup aborted." >&2
    exit 1
fi

# Check Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "[$(date)] ERROR: Docker not running. Backup aborted." >&2
    exit 1
fi

# Check DB container is up
if ! docker ps --format '{{.Names}}' | grep -q '^court_db_dev$'; then
    echo "[$(date)] ERROR: court_db_dev container not running. Backup aborted." >&2
    exit 1
fi

mkdir -p "$BACKUP_DIR"

docker exec court_db_dev pg_dump -U jonah courtdb_dev | gzip > "$BACKUP_DIR/$FILENAME"

SIZE=$(du -sh "$BACKUP_DIR/$FILENAME" | cut -f1)
echo "[$(date)] Backup written: $FILENAME ($SIZE)"

# Remove backups older than KEEP_DAYS days
find "$BACKUP_DIR" -name "courtdb_*.sql.gz" -mtime +$KEEP_DAYS -delete
echo "[$(date)] Cleaned up backups older than $KEEP_DAYS days"
