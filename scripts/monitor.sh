#!/bin/bash
# Health monitor: disk, CPU, memory and failed SSH logins -> Discord alert
# Usage: ./monitor.sh        (normal check)
#        ./monitor.sh test   (always sends a test alert)

WEBHOOK_URL=$(cat "$HOME/.discord_webhook")
HOST=$(hostname)

DISK_LIMIT=80
CPU_LIMIT=80
MEM_LIMIT=80
SSH_LIMIT=5

ALERTS=""

# 1. Disk usage (%) of the root filesystem
DISK=$(df / --output=pcent | tail -1 | tr -dc '0-9')
if [ "$DISK" -ge "$DISK_LIMIT" ]; then
    ALERTS+="Disk usage is ${DISK}% (limit ${DISK_LIMIT}%)\n"
fi

# 2. CPU load: 1-minute load average as % of CPU cores
LOAD=$(cut -d ' ' -f1 /proc/loadavg)
CORES=$(nproc)
CPU=$(awk -v l="$LOAD" -v c="$CORES" 'BEGIN { printf "%d", l / c * 100 }')
if [ "$CPU" -ge "$CPU_LIMIT" ]; then
    ALERTS+="CPU load is ${CPU}% (limit ${CPU_LIMIT}%)\n"
fi

# 3. Memory usage (%)
MEM=$(free | awk '/Mem:/ { printf "%d", $3 / $2 * 100 }')
if [ "$MEM" -ge "$MEM_LIMIT" ]; then
    ALERTS+="Memory usage is ${MEM}% (limit ${MEM_LIMIT}%)\n"
fi

# 4. Failed SSH login attempts in the last 5 minutes
SSH_FAILS=$(journalctl -u ssh --since "5 minutes ago" --no-pager 2>/dev/null \
    | grep -cE "Invalid user|Failed password|authenticating user" || true)
if [ "$SSH_FAILS" -ge "$SSH_LIMIT" ]; then
    ALERTS+="${SSH_FAILS} failed SSH login attempts in the last 5 minutes\n"
fi

# Test mode
if [ "$1" == "test" ]; then
    ALERTS+="Test alert (manual run)\n"
fi

# Send alert to Discord if anything was found
if [ -n "$ALERTS" ]; then
    MESSAGE=":warning: **Alert from ${HOST}**\n${ALERTS}"
    curl -s -H "Content-Type: application/json" \
        -d "{\"content\": \"${MESSAGE}\"}" \
        "$WEBHOOK_URL" > /dev/null
    echo "$(date): ALERT sent"
else
    echo "$(date): OK - disk ${DISK}%, cpu ${CPU}%, mem ${MEM}%, ssh fails ${SSH_FAILS}"
fi
