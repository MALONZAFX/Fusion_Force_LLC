FROM python:3.11-slim-bookworm

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Running migrations..."\n\
python manage.py migrate\n\
echo "Starting Gunicorn on port \$PORT..."\n\
exec gunicorn fusion_force.wsgi:application --bind 0.0.0.0:\$PORT --workers 2 --timeout 120\n' > /app/start.sh && chmod +x /app/start.sh

# Use this as the command
CMD ["/app/start.sh"]