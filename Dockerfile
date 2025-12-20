FROM python:3.11-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
COPY start.sh .
RUN chmod +x start.sh
CMD ["/app/start.sh"]