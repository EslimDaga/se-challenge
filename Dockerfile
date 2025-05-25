# Multi-stage build para desarrollo y producción
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        pkg-config \
        default-libmysqlclient-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure alembic.ini has correct permissions
RUN chmod 644 alembic.ini

# Create non-root user for security
RUN addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    && chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Development stage
FROM base AS development
ENV ENVIRONMENT=development
# Para desarrollo local forzamos puerto 8000
EXPOSE 8000
# Para desarrollo con hot reload
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

# Production stage
FROM base AS production
ENV ENVIRONMENT=production
# NO definir PORT aquí - Cloud Run lo maneja automáticamente
EXPOSE 8080

# Health check usando variable PORT dinámica
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Para producción - usar variable PORT dinámica
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1"]