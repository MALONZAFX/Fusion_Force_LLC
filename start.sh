#!/bin/bash
set -e

echo "=== STARTING DJANGO ON RAILWAY ==="
echo "PORT: $PORT"

python manage.py migrate --no-input
python manage.py collectstatic --no-input

exec gunicorn fusion_force.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
