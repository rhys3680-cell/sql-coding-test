#!/usr/bin/env bash
# Pagila 샘플 DB SQL 파일을 infra/init/ 에 다운로드.
# 최초 1회만 실행. 이후 docker compose 가 init 스크립트를 자동 적용.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INIT_DIR="$REPO_ROOT/infra/init"
BASE_URL="https://raw.githubusercontent.com/devrimgunduz/pagila/master"

mkdir -p "$INIT_DIR"

download() {
  local src="$1" dst="$2"
  if [[ -f "$dst" ]]; then
    echo "skip (exists): $dst"
    return
  fi
  echo "download: $src"
  curl -sSL -o "$dst" "$src"
}

download "$BASE_URL/pagila-schema.sql" "$INIT_DIR/01-pagila-schema.sql"
download "$BASE_URL/pagila-data.sql"   "$INIT_DIR/02-pagila-data.sql"

echo
echo "done. files in $INIT_DIR:"
ls -lh "$INIT_DIR"