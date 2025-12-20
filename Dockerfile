FROM python:3.11-slim-bookworm

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Remove the infinite loop script - Railway will use its own command
# Just expose the port
EXPOSE 8000

# Default command (Railway will override with its startCommand)
CMD ["gunicorn", "fusion_force.wsgi:application", "--bind", "0.0.0.0:8000"]