FROM python:3.11-slim-bookworm

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput

# Script is created inside Dockerfile
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Running migrations..."\n\
python manage.py migrate\n\
PORT=${PORT:-8000}\n\
echo "Starting Gunicorn on port $PORT..."\n\
exec gunicorn fusion_force.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120\n' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]