FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /tmp/uploads /tmp/outputs templates

# Copy application files
COPY xml_translator.py .
COPY app.py .
COPY templates/ templates/

# Create a non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app /tmp/uploads /tmp/outputs
USER appuser

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

# Run the application
CMD ["python", "app.py"]
