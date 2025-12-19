FROM python:3.11-slim-bookworm

WORKDIR /app

# Install dependencies including curl for debugging
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static
RUN python manage.py collectstatic --noinput

# Create a script that tests everything
RUN echo '#!/bin/bash\n\
set -x  # Enable debugging\n\
echo "=== STARTING DEBUG SESSION ==="\n\
echo "Current directory: $(pwd)"\n\
echo "Files in /app:"\n\
ls -la /app\n\
echo "\nFiles in /app/fusion_force:"\n\
ls -la /app/fusion_force\n\
echo "\n=== TESTING DJANGO ==="\n\
python manage.py check || echo "Django check failed"\n\
echo "\n=== TESTING WSGI ==="\n\
python -c "import sys; sys.path.insert(0, \"/app\"); from fusion_force.wsgi import application; print(\"WSGI import successful\")" || echo "WSGI import failed"\n\
echo "\n=== STARTING GUNICORN ==="\n\
PORT=${PORT:-8080}\n\
echo "Using port: $PORT"\n\
exec gunicorn fusion_force.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --log-level debug --access-logfile - --error-logfile -\n' > /app/debug.sh && chmod +x /app/debug.sh

CMD ["/app/debug.sh"]