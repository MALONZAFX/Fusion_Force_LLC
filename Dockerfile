# Dockerfile
FROM python:3.11-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files during build (no database needed)
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD python manage.py migrate && gunicorn fusion_force.wsgi --bind 0.0.0.0:$PORT