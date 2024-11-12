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

# Create the database directory
RUN mkdir -p database

# Expose port 5000
EXPOSE 5000

# Environment variables can be set here with defaults
ENV BASIC_AUTH_USERNAME=admin
ENV BASIC_AUTH_PASSWORD=password

# Switch to non-root user for better security
RUN useradd -m smartarts
USER smartarts

# Use Gunicorn instead of Flask's development server
# -w 4: 4 worker processes
# -b 0.0.0.0:5000: bind to all interfaces on port 5000
# --access-logfile -: log to stdout
# --error-logfile -: log errors to stdout
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "--access-logfile=-", "--error-logfile=-", "wsgi:app"]