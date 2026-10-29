#!/usr/bin/env zsh
# Starts the local Plane stack after login and verifies the API endpoint used by PKA.

set -u

export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

PKA_DIR="/Users/jchavauxm5/PKA_JCH"
PLANE_DIR="$PKA_DIR/_local/plane-community/plane-app"
ENV_FILE="$PLANE_DIR/plane.env"
LOG_FILE="$PKA_DIR/tmp/plane-autostart.log"
API_URL="http://127.0.0.1:8088/api/v1/"
MAX_WAIT_DOCKER_SECONDS="${PKA_PLANE_WAIT_DOCKER_SECONDS:-180}"
MAX_WAIT_API_SECONDS="${PKA_PLANE_WAIT_API_SECONDS:-240}"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
  printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG_FILE"
}

docker_ready() {
  docker info >/dev/null 2>&1
}

api_ready() {
  local http_code
  http_code="$(curl --silent --output /dev/null --write-out '%{http_code}' --max-time 3 "$API_URL" 2>/dev/null || true)"
  [[ "$http_code" =~ '^[0-9]{3}$' ]] && (( http_code < 500 ))
}

wait_until() {
  local max_seconds="$1"
  local check_name="$2"
  local start
  start="$(date +%s)"

  while true; do
    if "$check_name"; then
      return 0
    fi

    if (( "$(date +%s)" - start >= max_seconds )); then
      return 1
    fi

    sleep 5
  done
}

log "Plane autostart requested"

if [[ ! -d "$PLANE_DIR" ]]; then
  log "ERROR missing Plane directory: $PLANE_DIR"
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  log "ERROR missing Plane env file: $ENV_FILE"
  exit 1
fi

if ! docker_ready; then
  log "Docker is not ready; trying to start Docker Desktop"
  open -ga Docker >/dev/null 2>&1 || true
fi

if ! wait_until "$MAX_WAIT_DOCKER_SECONDS" docker_ready; then
  log "ERROR Docker daemon did not become ready within ${MAX_WAIT_DOCKER_SECONDS}s"
  exit 2
fi

log "Docker is ready; starting Plane compose stack"
cd "$PKA_DIR" || exit 1

docker compose -f "$PLANE_DIR/docker-compose.yaml" --env-file="$ENV_FILE" up -d >> "$LOG_FILE" 2>&1
compose_status="$?"
if [[ "$compose_status" != "0" ]]; then
  log "ERROR docker compose up failed with exit code $compose_status"
  exit "$compose_status"
fi

if wait_until "$MAX_WAIT_API_SECONDS" api_ready; then
  log "Plane API is reachable at $API_URL"
  exit 0
fi

log "WARNING Plane compose is up but API did not become reachable within ${MAX_WAIT_API_SECONDS}s"
exit 3
