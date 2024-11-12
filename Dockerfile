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

# Command to run the application
CMD ["python", "app.py"]