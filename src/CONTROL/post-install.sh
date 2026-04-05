#!/bin/sh

PKG_NAME="LibreSpeedtest"
PKG_ROOT="/usr/local/AppCentral/${PKG_NAME}"
VAR_DIR="${PKG_ROOT}/var"
LOG_FILE="${VAR_DIR}/install.log"

log_message() {
    mkdir -p "${VAR_DIR}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "${LOG_FILE}" 2>/dev/null || echo "$1"
}

log_message "Post-installation starting for package: ${PKG_NAME}"

# Create runtime var directory
if mkdir -p "${VAR_DIR}"; then
    log_message "Created var directory: ${VAR_DIR}"
    chmod 755 "${VAR_DIR}"
else
    log_message "Error: Failed to create var directory: ${VAR_DIR}"
    exit 1
fi

# Create lighttpd config for our dedicated port
cat > "${VAR_DIR}/lighttpd.conf" << EOF
server.modules = ( "mod_cgi" )
server.document-root = "${PKG_ROOT}/webman"
server.port = 39878
server.pid-file = "${VAR_DIR}/lighttpd.pid"
server.errorlog = "${VAR_DIR}/httpd.log"
index-file.names = ( "index.html" )
cgi.assign = ( ".cgi" => "" )
static-file.exclude-extensions = ( ".cgi" )
server.stream-request-body = 2
server.stream-response-body = 2
EOF
chmod 644 "${VAR_DIR}/lighttpd.conf"
log_message "Created lighttpd.conf"

# Set execute permissions for CGI scripts
chmod +x "${PKG_ROOT}/webman/backend/garbage.cgi" && \
    log_message "Set +x on webman/backend/garbage.cgi" || \
    { log_message "Warning: webman/backend/garbage.cgi not found"; ERRORS=1; }

chmod +x "${PKG_ROOT}/webman/backend/empty.cgi" && \
    log_message "Set +x on webman/backend/empty.cgi" || \
    { log_message "Warning: webman/backend/empty.cgi not found"; ERRORS=1; }

chmod +x "${PKG_ROOT}/webman/backend/getIP.cgi" && \
    log_message "Set +x on webman/backend/getIP.cgi" || \
    { log_message "Warning: webman/backend/getIP.cgi not found"; ERRORS=1; }

if [ -z "${ERRORS}" ]; then
    log_message "Post-installation completed successfully"
else
    log_message "Post-installation completed with warnings"
fi
echo >> "${LOG_FILE}"
exit 0
