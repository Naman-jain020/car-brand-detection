# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p static/raw_images

# Expose port (Railway will override)
EXPOSE 5000

# Run with gunicorn (Railway sets $PORT automatically)
CMD gunicorn --bind 0.0.0.0:$PORT run:app
