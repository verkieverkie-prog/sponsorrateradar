#!/bin/bash
cd "$(dirname "$0")/.."
mkdir -p /tmp/prev
rm -rf /tmp/prev/sponsorrateradar
cp -r site /tmp/prev/sponsorrateradar
if ! curl -s -o /dev/null http://localhost:8799/; then
  nohup python3 -m http.server 8799 --directory /tmp/prev > /tmp/http.log 2>&1 &
  sleep 1
fi
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8799/sponsorrateradar/
