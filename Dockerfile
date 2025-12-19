FROM python:3.11-slim-bookworm

# Install wait-for-it script to handle Railway's startup timing
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Collect static
RUN python manage.py collectstatic --noinput

# Create a startup script that Railway won't kill
RUN echo '#!/bin/bash\n\
# Force immediate response to Railway health checks\n\
echo "Starting application..." > /tmp/startup.log\n\
\n\
# Start Django in background\n\
python manage.py runserver 0.0.0.0:$PORT > /tmp/django.log 2>&1 &\n\
DJANGO_PID=$!\n\
\n\
# Keep container alive with a simple HTTP server on port 8081\n\
python -m http.server 8081 --directory /app > /tmp/health.log 2>&1 &\n\
HEALTH_PID=$!\n\
\n\
# Wait forever\n\
echo "Application started. PIDs: Django=$DJANGO_PID, Health=$HEALTH_PID" >> /tmp/startup.log\n\
tail -f /tmp/startup.log\n\
wait $DJANGO_PID\n' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]