# =========================================================================
# Project 35: Crop Disease Expert System - Dockerfile
# Lightweight, secure container image for interactive CLI execution
# =========================================================================

FROM python:3.11-slim

# Set environment variables for Python in Docker
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set container working directory
WORKDIR /app

# Copy dependency definition first to optimize Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and knowledge base
COPY app.py inference.py build_kb.py knowledge_base.json knowledge_base_rules.csv ./
COPY tests/ ./tests/
COPY docs/ ./docs/

# Create a non-root application user for secure container execution
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Configure entrypoint to launch the CLI expert system
ENTRYPOINT ["python", "app.py"]

# Default command (interactive CLI menu)
CMD []
