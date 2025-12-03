#!/bin/bash
set -e

echo "=== Starting Fusion Force LLC ==="

# Set default port if $PORT not set
PORT=${PORT:-8080}
echo "Using port: $PORT"

# Debug info
echo "Python: $(python --version)"
echo "Django: $(python -c \"import django; print(django.get_version())\")"

# Show migration files
echo "Migration files in main/migrations/:"
ls -la main/migrations/ || echo "No migrations directory found"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput || echo "Migrations failed, continuing..."

# Start server with proper port
echo "Starting Gunicorn on port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 --access-logfile - --error-logfile - yourproject.wsgi:application