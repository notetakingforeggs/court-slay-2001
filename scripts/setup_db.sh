#!/bin/bash
set -e

COMPOSE_FILE="$(dirname "$0")/../docker-compose.dev.yaml"
MIGRATIONS_DIR="$(dirname "$0")/../db/migrations"
DB_CONTAINER="court_db_dev"
DB_USER="jonah"
DB_NAME="courtdb_dev"

echo "Starting postgres..."
docker compose -f "$COMPOSE_FILE" up -d postgres

echo "Waiting for postgres to be healthy..."
until docker exec "$DB_CONTAINER" pg_isready -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; do
    sleep 1
done
echo "Postgres is ready."

echo "Running schema migration..."
docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "
    CREATE TABLE IF NOT EXISTS region (id bigint PRIMARY KEY, region_name varchar(255));
    CREATE TABLE IF NOT EXISTS court (id bigint PRIMARY KEY, city varchar(255), name varchar(255), region_id bigint NOT NULL REFERENCES region(id));
    CREATE TABLE IF NOT EXISTS court_case (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        start_time_epoch bigint NOT NULL,
        court_id bigint NOT NULL REFERENCES court(id),
        case_id varchar(255),
        claimant varchar(255),
        defendant varchar(255),
        duration bigint,
        hearing_channel varchar(255),
        hearing_type varchar(255),
        case_details text,
        created_at bigint,
        is_minor boolean,
        UNIQUE (court_id, case_id, start_time_epoch)
    );
    CREATE SEQUENCE IF NOT EXISTS subscription_seq START WITH 1 INCREMENT BY 50;
    CREATE TABLE IF NOT EXISTS subscription (
        id bigint PRIMARY KEY DEFAULT nextval('subscription_seq'),
        chat_id bigint,
        alert_terms_claimant varchar(255)[],
        alert_terms_defendant varchar(255)[],
        last_notified_timestamp bigint
    );
"

echo "Seeding reference data..."
docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" < "$MIGRATIONS_DIR/R__seed_reference_data.sql"

echo "Done. Starting remaining services..."
docker compose -f "$COMPOSE_FILE" up -d
