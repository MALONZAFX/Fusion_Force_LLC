# Dockerfile - Optimized for Railway deployment
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies with proper cleanup
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files during build
RUN python manage.py collectstatic --noinput

# Create non-root user for security (optional but recommended)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check (for Railway health monitoring)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:$PORT/health/', timeout=2)"

# Run migrations and start gunicorn
CMD python manage.py migrate --noinput && \
    gunicorn fusion_force.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --worker-class sync \
    --timeout 120 \
    --access-logfile -