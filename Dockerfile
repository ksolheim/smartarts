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

# Copy entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Create a user with default UID/GID
RUN groupadd -g 1000 smartarts && \
    useradd -m -u 1000 -g 1000 smartarts && \
    chown -R smartarts:smartarts /app/database && \
    apt-get update && apt-get install -y gosu && rm -rf /var/lib/apt/lists/*

# Use entrypoint script
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Use Gunicorn instead of Flask's development server
# -w 4: 4 worker processes
# -b 0.0.0.0:5000: bind to all interfaces on port 5000
# --access-logfile -: log to stdout
# --error-logfile -: log errors to stdout
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "--access-logfile=-", "--error-logfile=-", "wsgi:app"]