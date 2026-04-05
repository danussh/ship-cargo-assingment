# Multi-stage build for smaller image size
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

# Create non-root user for security
RUN useradd -m -u 1000 shipiq && \
    mkdir -p /app && \
    chown -R shipiq:shipiq /app

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder --chown=shipiq:shipiq /root/.local /home/shipiq/.local

# Copy application code
COPY --chown=shipiq:shipiq ./app ./app
COPY --chown=shipiq:shipiq ./static ./static
COPY --chown=shipiq:shipiq .env.example .env

# Update PATH
ENV PATH=/home/shipiq/.local/bin:$PATH

# Switch to non-root user
USER shipiq

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')"

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
