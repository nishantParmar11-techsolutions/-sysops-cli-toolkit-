# ==============================================================================
# SysOps CLI Toolkit - Master-Class Secure Production Dockerfile
# ==============================================================================

# --- Stage 1: Build & Dependencies Stage ---
FROM python:3.10-slim AS builder

WORKDIR /build

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install essential build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies and package
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .


# --- Stage 2: Final Lean Runtime Stage ---
FROM python:3.10-slim AS runtime

WORKDIR /app

# Create a secure non-root system user for enterprise security compliance
RUN groupadd -r sysops && useradd -r -g sysops sysops

# Copy installed site-packages and binaries from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application source code and documentation
COPY main.py test_main.py README.md ./

# Change ownership of application files to the non-root user
RUN chown -R sysops:sysops /app

# Switch to the non-root user for all runtime executions
USER sysops

# Default Entrypoint & Command
ENTRYPOINT ["sysops"]
CMD ["system-info"]
