#!/bin/sh
# LibreSpeed download test backend
# Replaces garbage.php - streams random bytes to measure download speed
# Called by speedtest.js as: backend/garbage.cgi?ckSize=N  (N = chunks of 1 MiB)

# Parse ckSize from QUERY_STRING (default 4, max 1024)
ckSize=4
if [ -n "$QUERY_STRING" ]; then
    val=$(echo "$QUERY_STRING" | sed 's/.*ckSize=\([0-9]*\).*/\1/')
    if echo "$val" | grep -qE '^[0-9]+$'; then
        if [ "$val" -gt 0 ] && [ "$val" -le 1024 ]; then
            ckSize=$val
        elif [ "$val" -gt 1024 ]; then
            ckSize=1024
        fi
    fi
fi

# Calculate total bytes: ckSize * 1 MiB
bytes=$((ckSize * 1048576))

printf 'Content-Description: File Transfer\r\n'
printf 'Content-Type: application/octet-stream\r\n'
printf 'Content-Disposition: attachment; filename=random.dat\r\n'
printf 'Content-Transfer-Encoding: binary\r\n'
printf 'Content-Length: %d\r\n' "$bytes"
printf 'Cache-Control: no-store, no-cache, must-revalidate, max-age=0\r\n'
printf 'Pragma: no-cache\r\n'
printf '\r\n'

dd if=/dev/urandom bs=1048576 count="$ckSize" 2>/dev/null
