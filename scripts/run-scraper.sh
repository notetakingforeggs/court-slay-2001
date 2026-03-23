#!/bin/bash

cd ~/dev/court-slay-2001 || exit 1

docker compose -f docker-compose.dev.yaml run scraper
