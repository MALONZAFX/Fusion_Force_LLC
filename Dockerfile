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

# Debug: Show what files are copied
RUN echo "=== Migration Files Check ===" && \
    ls -la main/migrations/ && \
    echo "=== End Check ==="

# Run migrations
RUN python manage.py migrate --noinput

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Start server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "yourproject.wsgi:application"]