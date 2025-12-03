FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Start server - NO MIGRATIONS
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "fusion_force.wsgi:application"]