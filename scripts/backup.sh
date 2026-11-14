#!/bin/bash
# Backup script: database dump + API logs, keeps the last 7 days 
set -e
set -o pipefail

APP_DIR="/home/deploy/app"
BACKUP_DIR="/home/deploy/backups"
DATE=$(date +%Y-%m-%d_%H-%M)
KEEP_DAYS=7

mkdir -p "$BACKUP_DIR"
cd "$APP_DIR"

# Read DATABASE_NAME from .env
source "$APP_DIR/.env"

# 1. Database backup
docker compose exec -T db pg_dump -U postgres "$DATABASE_NAME" | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# 2. API logs backup
docker compose logs --no-color api | gzip > "$BACKUP_DIR/api_logs_$DATE.log.gz"

# 3. Delete backups older than KEEP_DAYS
find "$BACKUP_DIR" -type f -name "*.gz" -mtime +$KEEP_DAYS -delete

echo "$(date): Backup done -> $BACKUP_DIR"
