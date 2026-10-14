# Production & Development Dockerfile for JAMES Building-Aware Digital Twin
FROM python:3.11-slim

# Install system dependencies (Graphviz required for Single-Line Diagram DOT compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Environment Defaults (Overrideable via docker-compose or GCP Cloud Run env)
ENV HOST=0.0.0.0 \
    PORT=8000 \
    JAMES_DATA_DIR=/app/data \
    PYTHONUNBUFFERED=1

# Expose web service port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/catalog || exit 1

# Start FastAPI application with Uvicorn entrypoint (dynamically respecting PORT/HOST)
CMD ["python", "-m", "james_app"]
