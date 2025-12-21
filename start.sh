#!/bin/bash
echo "=== STARTING DJANGO ON RAILWAY ==="
echo "PORT: $PORT"
echo "PWD: $(pwd)"
echo "Files: $(ls -la)"

# Run migrations
python manage.py migrate

# Start Gunicorn with explicit logging
exec gunicorn fusion_force.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug