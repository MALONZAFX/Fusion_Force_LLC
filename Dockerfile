FROM python:3.11-slim

WORKDIR /app

# Install ONLY what we need
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create empty SQLite database file
RUN touch /tmp/db.sqlite3

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Start server - NO MIGRATIONS, NO DATABASE CHECKS
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "fusion_force.wsgi:application"]