#!/usr/bin/env bash
# KETI WorkOS 웹 대시보드 — Cursor 종료 후에도 계속 서빙
set -euo pipefail

WEB_DIR="$(cd "$(dirname "$0")/../web" && pwd)"
SERVICE="keti-workos-web.service"

usage() {
  cat <<'EOF'
Usage: ./scripts/web-serve.sh <command>

Commands:
  start    빌드 후 백그라운드 서비스 시작 (systemd)
  stop     서비스 중지
  restart  재빌드 후 재시작
  status   서비스 상태 확인
  logs     최근 로그 보기
  dev      개발 서버 (LAN, Cursor 안에서만 — 종료 시 같이 꺼짐)
EOF
}

cmd_start() {
  echo "→ npm run build"
  (cd "$WEB_DIR" && npm run build)
  systemctl --user daemon-reload
  systemctl --user enable "$SERVICE"
  systemctl --user start "$SERVICE"
  systemctl --user --no-pager status "$SERVICE" || true
  echo ""
  echo "접속: http://$(hostname -I | awk '{print $1}'):5173/"
}

cmd_restart() {
  (cd "$WEB_DIR" && npm run build)
  systemctl --user restart "$SERVICE"
  systemctl --user --no-pager status "$SERVICE" || true
}

case "${1:-}" in
  start) cmd_start ;;
  stop) systemctl --user stop "$SERVICE" ;;
  restart) cmd_restart ;;
  status) systemctl --user --no-pager status "$SERVICE" ;;
  logs) journalctl --user -u "$SERVICE" -n 40 --no-pager ;;
  dev) cd "$WEB_DIR" && npm run dev:lan ;;
  *) usage; exit 1 ;;
esac
