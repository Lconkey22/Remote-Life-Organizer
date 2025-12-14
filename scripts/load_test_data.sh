#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"

curl_json() {
  local method="$1"
  local path="$2"
  local json="$3"

  curl -sS --fail \
    -X "$method" \
    -H "Content-Type: application/json" \
    "$BASE_URL$path" \
    -d "$json"
}

curl_get() {
  local path="$1"
  curl -sS --fail "$BASE_URL$path"
}

echo "Using BASE_URL=$BASE_URL"

echo "Checking server..."
curl_get "/homepage" >/dev/null

echo "Loading tasks..."
curl_json POST "/tasks/" '{"title":"Finish CIS module","due_date":"2025-12-20T12:00:00","completed":false}'
echo
curl_json POST "/tasks/" '{"title":"Follow up on discussion post","due_date":"2025-12-22T18:00:00","completed":false}'
echo
curl_json POST "/tasks/" '{"title":"Plan week","due_date":"2025-12-19T09:00:00","completed":true}'
echo

echo "Loading events..."
curl_json POST "/events/" '{"name":"Meal Prep","type":"Other","start_time":"2025-12-14T12:00:00","end_time":"2025-12-14T13:00:00"}'
echo
curl_json POST "/events/" '{"name":"Morning Run","type":"Self Care","start_time":"2025-12-15T08:30:00","end_time":"2025-12-15T09:15:00"}'
echo
curl_json POST "/events/" '{"name":"Office Hours","type":"Work","start_time":"2025-12-16T10:00:00","end_time":"2025-12-16T12:00:00"}'
echo
curl_json POST "/events/" '{"name":"Study CIS","type":"Homework","start_time":"2025-12-17T09:00:00","end_time":"2025-12-17T11:00:00"}'
echo
curl_json POST "/events/" '{"name":"Therapy Appointment","type":"Self Care","start_time":"2025-12-18T13:00:00","end_time":"2025-12-18T14:00:00"}'
echo
curl_json POST "/events/" '{"name":"Project Sprint","type":"Work","start_time":"2025-12-19T11:00:00","end_time":"2025-12-19T15:00:00"}'
echo
curl_json POST "/events/" '{"name":"Team Meeting","type":"Work","start_time":"2025-12-20T15:00:00","end_time":"2025-12-20T16:00:00"}'
echo
curl_json POST "/events/" '{"name":"Work on Python Assignment","type":"Homework","start_time":"2025-12-21T10:00:00","end_time":"2025-12-21T12:00:00"}'
echo
curl_json POST "/events/" '{"name":"Family Dinner","type":"Family","start_time":"2025-12-22T18:30:00","end_time":"2025-12-22T20:00:00"}'
echo
curl_json POST "/events/" '{"name":"Haircut","type":"Other","start_time":"2025-12-23T14:00:00","end_time":"2025-12-23T15:00:00"}'
echo

echo "Loading homework..."
curl_json POST "/homework/" '{"course":"Math","due_date":"2025-12-21","description":"Problem set 1","completed":false}'
echo
curl_json POST "/homework/" '{"course":"CIS","due_date":"2025-12-22","description":"Discussion post","completed":false}'
echo
curl_json POST "/homework/" '{"course":"English","due_date":"2025-12-20","description":"Read chapter 3","completed":true}'
echo

echo "Loading time entries..."
curl_json POST "/time-entries/" '{"type":"Work","start_time":"2025-12-20T09:00:00","end_time":"2025-12-20T11:30:00","note":"Deep work"}'
echo
curl_json POST "/time-entries/" '{"type":"Homework","start_time":"2025-12-21T13:00:00","end_time":"2025-12-21T14:15:00","note":"Study session"}'
echo
curl_json POST "/time-entries/" '{"type":"Other","start_time":"2025-12-22T07:30:00","end_time":"2025-12-22T08:00:00","note":"Morning planning"}'
echo

echo "Done. Current homepage snapshot:"
curl_get "/homepage?days=14&tasks_limit=10&events_limit=10"
echo
