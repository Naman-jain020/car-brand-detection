# # Multi-stage build to reduce image size
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /root/.local /root/.local

# Add user site-packages to PATH
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app ./app
COPY scripts ./scripts
COPY templates ./templates
COPY visualize ./visualize
COPY model ./model
COPY static ./static
COPY run.py .

# Create directories
RUN mkdir -p static/raw_images

# Expose port
EXPOSE 5000

# Run application
CMD gunicorn --bind 0.0.0.0:$PORT run:app
