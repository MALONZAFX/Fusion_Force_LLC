# Dockerfile - DEBUG VERSION
FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create a simple test Python script
RUN echo 'import os\nimport sys\nsys.path.insert(0, "/app")\n\nfrom django.core.wsgi import get_wsgi_application\nos.environ.setdefault("DJANGO_SETTINGS_MODULE", "fusion_force.settings")\napplication = get_wsgi_application()\n\n# Simple HTTP server for testing\nfrom http.server import HTTPServer, BaseHTTPRequestHandler\nclass Handler(BaseHTTPRequestHandler):\n    def do_GET(self):\n        self.send_response(200)\n        self.end_headers()\n        self.wfile.write(b"DEBUG: App is working!")\n\nPORT = int(os.getenv("PORT", 8080))\nprint(f"Starting debug server on port {PORT}")\nHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()' > /app/debug_server.py

# Start with simple Python server first
CMD python /app/debug_server.py