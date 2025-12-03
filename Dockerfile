FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ALL project files
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port 8080 (Railway's default)
EXPOSE 8080

# Create startup script that runs migrations THEN starts server
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "=== Starting Fusion Force LLC ==="\n\
\n\
# Run migrations\n\
echo "Running migrations..."\n\
python manage.py migrate --noinput\n\
\n\
# Collect static files\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput --clear\n\
\n\
# Start server\n\
echo "Starting Gunicorn on port 8080..."\n\
exec gunicorn --bind 0.0.0.0:8080 --workers 3 --access-logfile - --error-logfile - fusionforce.wsgi:application\n\
' > /app/start.sh && chmod +x /app/start.sh

# Use the startup script
CMD ["/app/start.sh"]