#!/bin/sh
# LibreSpeed IP detection backend
# Replaces getIP.php - returns client IP address as JSON
# speedtest.js displays this in the UI after the test

# Determine client IP - check proxy headers first, fall back to REMOTE_ADDR
ip=""
if [ -n "$HTTP_CLIENT_IP" ]; then
    ip="$HTTP_CLIENT_IP"
elif [ -n "$HTTP_X_REAL_IP" ]; then
    ip="$HTTP_X_REAL_IP"
elif [ -n "$HTTP_X_FORWARDED_FOR" ]; then
    # X-Forwarded-For can be comma-separated; client IP is first
    ip=$(echo "$HTTP_X_FORWARDED_FOR" | cut -d',' -f1 | tr -d ' ')
else
    ip="$REMOTE_ADDR"
fi

# Strip IPv4-mapped IPv6 prefix (::ffff:x.x.x.x -> x.x.x.x)
ip=$(echo "$ip" | sed 's/^::ffff://')

# Return JSON matching what speedtest.js expects:
# { "processedString": "ip - info", "rawIspInfo": "" }
# For a LAN-only setup we just return the IP; no ISP lookup needed
json="{\"processedString\":\"${ip}\",\"rawIspInfo\":\"\"}"

printf 'Content-Type: application/json; charset=utf-8\r\n'
printf 'Cache-Control: no-store, no-cache, must-revalidate, max-age=0\r\n'
printf 'Pragma: no-cache\r\n'
printf '\r\n'
printf '%s' "$json"
