FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Make sure migrations directory exists
RUN mkdir -p main/migrations && touch main/migrations/__init__.py

# Create migrations and run them
RUN python manage.py makemigrations main --noinput
RUN python manage.py migrate --noinput

# Start server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "yourproject.wsgi"]