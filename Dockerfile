# Multi-stage build for production optimization
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy requirements first for better caching
COPY pyproject.toml setup.py ./
COPY elevenlabs_mcp/__init__.py elevenlabs_mcp/__init__.py

# Install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -e .

# Copy the rest of the application
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Create output and shared directories with proper permissions
RUN mkdir -p /app/output /app/shared && chown -R appuser:appuser /app/output /app/shared

# Switch to non-root user
USER appuser

# Expose port (configurable via environment)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -s http://localhost:3000/mcp > /dev/null || exit 1

# Use environment variables for configuration
ENV ELEVENLABS_MCP_BASE_PATH=/app/shared
ENV HOST=0.0.0.0
ENV PORT=3000

# Command to run the server (can be overridden)
CMD ["python", "-m", "elevenlabs_mcp", "--server"]