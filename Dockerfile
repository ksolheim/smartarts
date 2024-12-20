# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# Use Gunicorn instead of Flask's development server
# -w 4: 4 worker processes
# -b 0.0.0.0:5000: bind to all interfaces on port 5000
# --access-logfile -: log to stdout
# --error-logfile -: log errors to stdout
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "--timeout=120", "--keep-alive=5", "--max-requests=1000", "--max-requests-jitter=50", "--access-logfile=-", "--error-logfile=-", "wsgi:app"]
