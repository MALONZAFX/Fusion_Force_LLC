# Dockerfile
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Start command - simple and reliable
CMD gunicorn fusion_force.wsgi:application --bind 0.0.0.0:$PORT --workers 1