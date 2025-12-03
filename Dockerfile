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

# Debug: Show migration files
RUN echo "=== DEBUG: Checking migration files ===" && \
    if [ -d "main/migrations" ]; then \
        echo "✓ migrations directory exists" && \
        ls -la main/migrations/ && \
        echo "Migration files found:" && \
        find main/migrations -name "*.py" -type f; \
    else \
        echo "✗ No migrations directory found" && \
        mkdir -p main/migrations && \
        touch main/migrations/__init__.py; \
    fi

# Create migrations if missing
RUN echo "=== Creating migrations ===" && \
    python manage.py makemigrations main --noinput || \
    echo "Migrations already exist or failed"

# Run ALL migrations
RUN echo "=== Running migrations ===" && \
    python manage.py migrate --noinput

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port 8080 (Railway's default)
EXPOSE 8080

# Start server with HARDCODED port 8080 (NOT $PORT)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "fusionforce.wsgi:application"]