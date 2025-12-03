FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# NO MIGRATIONS - JUST COLLECT STATICS
RUN python manage.py collectstatic --noinput --clear

# Start server WITHOUT any database checks
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "fusion_force.wsgi:application"]