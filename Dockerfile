FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "=== Starting Django Application ==="\n\
echo "Running migrations..."\n\
python manage.py migrate\n\
echo "Starting Gunicorn on port \$PORT..."\n\
exec gunicorn fusion_force.wsgi:application --bind 0.0.0.0:\$PORT --workers 3\n' > /app/start.sh && \
    chmod +x /app/start.sh

# Run as non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["/app/start.sh"]