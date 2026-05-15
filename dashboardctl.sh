#!/usr/bin/env zsh

set -euo pipefail

PKA_DIR="$(cd "$(dirname "$0")" && pwd)"
PORT="${PKA_DASHBOARD_PORT:-8787}"
HOST="${PKA_DASHBOARD_HOST:-127.0.0.1}"
RUNTIME_DIR="$PKA_DIR/tmp"
PID_FILE="$RUNTIME_DIR/dashboard.pid"
LOG_FILE="$RUNTIME_DIR/dashboard.log"
URL="http://$HOST:$PORT/hub.html"
LABEL="com.jchytech.pka-dashboard"
LAUNCH_AGENT_PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

mkdir -p "$RUNTIME_DIR"

launchd_installed() {
  [[ -f "$LAUNCH_AGENT_PLIST" ]]
}

launchd_loaded() {
  launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1
}

running_pid() {
  if [[ -f "$PID_FILE" ]]; then
    local pid
    pid="$(<"$PID_FILE")"
    if [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null; then
      echo "$pid"
      return 0
    fi
    rm -f "$PID_FILE"
  fi
  return 1
}

port_pid() {
  lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | head -n 1
}

launchd_pid() {
  launchctl print "gui/$(id -u)/$LABEL" 2>/dev/null | awk '/\bpid = / {print $3; exit}'
}

dashboard_pid_by_port() {
  local pid
  pid="$(port_pid || true)"
  if [[ -z "$pid" ]]; then
    return 1
  fi
  if ps -p "$pid" -o command= | grep -q "dashboard_server.py"; then
    echo "$pid"
    return 0
  fi
  return 1
}

wait_for_health() {
  for _ in {1..30}; do
    if curl -fsS "http://$HOST:$PORT/api/health" >/dev/null 2>&1; then
      return 0
    fi
    sleep 0.2
  done
  return 1
}

start_via_launchd() {
  local pid
  launchctl enable "gui/$(id -u)/$LABEL"
  launchctl kickstart -k "gui/$(id -u)/$LABEL"
  if wait_for_health; then
    pid="$(launchd_pid || true)"
    echo "Dashboard actif via launchd${pid:+ (PID $pid)}"
    echo "$URL"
    return 0
  fi
  echo "Le service launchd n'a pas demarre correctement. Voir tmp/dashboard.launchd.log"
  return 1
}

start_server() {
  local pid existing
  if launchd_installed; then
    start_via_launchd
    return 0
  fi

  if pid="$(running_pid)"; then
    echo "Dashboard deja actif (PID $pid)"
    echo "$URL"
    return 0
  fi

  existing="$(port_pid || true)"
  if [[ -n "$existing" ]]; then
    echo "Port $PORT deja occupe par PID $existing"
    echo "Liberer le port ou changer PKA_DASHBOARD_PORT."
    return 1
  fi

  nohup python3 "$PKA_DIR/scripts/dashboard_server.py" --host "$HOST" --port "$PORT" >>"$LOG_FILE" 2>&1 &
  pid=$!
  echo "$pid" > "$PID_FILE"

  if wait_for_health; then
    echo "Dashboard actif (PID $pid)"
    echo "$URL"
    return 0
  fi

  echo "Le serveur n'a pas demarre correctement. Voir $LOG_FILE"
  return 1
}

stop_server() {
  local pid
  if launchd_loaded; then
    launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
    rm -f "$PID_FILE"
    echo "Dashboard launchd arrete"
    return 0
  fi
  if pid="$(running_pid)"; then
    kill "$pid" 2>/dev/null || true
    for _ in {1..20}; do
      if ! kill -0 "$pid" 2>/dev/null; then
        rm -f "$PID_FILE"
        echo "Dashboard arrete"
        return 0
      fi
      sleep 0.1
    done
    kill -9 "$pid" 2>/dev/null || true
    rm -f "$PID_FILE"
    echo "Dashboard force arrete"
    return 0
  fi
  echo "Dashboard deja arrete"
}

status_server() {
  local pid
  if launchd_loaded; then
    pid="$(launchd_pid || true)"
    if curl -fsS "http://$HOST:$PORT/api/health" >/dev/null 2>&1; then
      echo "Dashboard actif via launchd${pid:+ (PID $pid)}"
      echo "$URL"
      return 0
    fi
    echo "Dashboard launchd charge mais indisponible"
    return 1
  fi
  if pid="$(running_pid)"; then
    echo "Dashboard actif (PID $pid)"
    echo "$URL"
    return 0
  fi
  echo "Dashboard inactif"
  return 1
}

open_server() {
  start_server
  open "$URL"
}

case "${1:-start}" in
  start)
    start_server
    ;;
  stop)
    stop_server
    ;;
  restart)
    stop_server || true
    start_server
    ;;
  status)
    status_server
    ;;
  open)
    open_server
    ;;
  logs)
    echo "$LOG_FILE"
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status|open|logs}"
    exit 1
    ;;
esac
