#!/bin/bash

echo "Starting scraper at $(date)" >> /home/jonah/development/code/court-slay-2000/logs/scraper-debug.log

export PATH=/usr/local/sbin:/usr/local/bin:/usr/bin:/sbin:/bin

cd /home/jonah/development/code/court-slay-2000 || exit 1

/usr/local/bin/docker compose run --rm scraper >> /home/jonah/development/code/court-slay-2000/logs/scraper.log 2>&1

echo "finished scraper at $(date)" >> /home/jonah/development/code/court-slay-2000/logs/scraper-debug.log
