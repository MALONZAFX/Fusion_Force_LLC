#!/bin/bash
set -e

echo "=== Starting Fusion Force LLC ==="

# Debug info
echo "Python: $(python --version)"
echo "Django: $(python -c \"import django; print(django.get_version())\")"

# Show migration files
echo "Migration files in main/migrations/:"
ls -la main/migrations/ || echo "No migrations directory found"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput || echo "Migrations failed, continuing..."

# Start server
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 --access-logfile - --error-logfile - yourproject.wsgi:application