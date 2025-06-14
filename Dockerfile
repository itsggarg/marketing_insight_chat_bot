# Marketing Insights Bot - Docker Configuration
# Multi-stage build for optimized production image

FROM python:3.10-slim

WORKDIR /app

# Set environment variables for Python optimization
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies required for MySQL client
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create directory for Cloud SQL socket (if using Google Cloud SQL)
RUN mkdir -p /cloudsql

# Upgrade pip and install Python dependencies
# Installing in specific order to handle dependencies correctly
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir numpy==1.24.3
RUN pip install --no-cache-dir pandas==2.0.3
RUN pip install --no-cache-dir \
    Flask==2.3.3 \
    openpyxl==3.1.2 \
    google-generativeai==0.3.2 \
    sqlalchemy==2.0.23 \
    mysql-connector-python==8.2.0 \
    python-dotenv==1.0.0 \
    gunicorn==21.2.0

# Copy application code
COPY . .

# Create required directories for templates and static files
RUN mkdir -p templates static

# Expose port for web service
EXPOSE 8080

# Use gunicorn for production deployment
# Configuration: 1 worker, 2 threads, 300s timeout for long-running AI requests
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "2", "--timeout", "300", "app:app"]
