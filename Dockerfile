FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# No migrations needed
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "fusion_force.wsgi:application"]