# Use Python 3.12 slim image to match your dev environment
FROM python:3.12-slim

# Set working directory to webapp folder
WORKDIR /app/webapp

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV FLASK_APP=app:app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for Tailwind CSS
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt gunicorn

# Copy and install Node.js dependencies
COPY package*.json /app/
WORKDIR /app
RUN npm ci --only=production

# Copy application code
COPY . /app/

# Switch back to webapp directory
WORKDIR /app/webapp

# Create necessary directories
RUN mkdir -p ../data ../backups

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Use Gunicorn for production - now from webapp directory
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]