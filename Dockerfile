FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# FORCE migrations to run (even if they appear applied)
RUN echo "Applying ALL migrations..." && \
    python manage.py migrate --run-syncdb --noinput

# Start server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "yourproject.wsgi:application"]