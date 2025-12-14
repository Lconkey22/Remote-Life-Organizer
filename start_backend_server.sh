#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"

echo "Starting FastAPI server..."
fastapi dev backend/main.py &
SERVER_PID=$!

echo "Waiting for server to be ready..."
for i in {1..30}; do
  if curl -sSf "$BASE_URL/homepage" >/dev/null 2>&1; then
    echo "Server is ready!"
    break
  fi
  if [ $i -eq 30 ]; then
    echo "Server did not become ready in time"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
  fi
  sleep 1
done

echo "Loading test data..."
bash "$SCRIPT_DIR/scripts/load_test_data.sh"

echo "Server is running (PID: $SERVER_PID). Press Ctrl+C to stop."
wait $SERVER_PID
