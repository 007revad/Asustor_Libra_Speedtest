#!/bin/sh
# LibreSpeed upload test and ping backend
# Replaces empty.php - reads and discards POST body, returns 200
# Used for both upload measurement and ping/jitter timing

# Must consume entire POST body before responding, otherwise browser XHR stalls
if [ "$REQUEST_METHOD" = "POST" ] && [ -n "$CONTENT_LENGTH" ] && [ "$CONTENT_LENGTH" -gt 0 ] 2>/dev/null; then
    dd bs=4096 count=$(( (CONTENT_LENGTH + 4095) / 4096 )) of=/dev/null 2>/dev/null
fi

printf 'Content-Type: text/plain\r\n'
printf 'Content-Length: 0\r\n'
printf 'Cache-Control: no-store, no-cache, must-revalidate, max-age=0\r\n'
printf 'Pragma: no-cache\r\n'
printf 'Connection: keep-alive\r\n'
printf '\r\n'
