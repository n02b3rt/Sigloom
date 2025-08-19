
# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# System deps (optional)
RUN apt-get update && apt-get install -y --no-install-recommends     ca-certificates curl && rm -rf /var/lib/apt/lists/*

# Python deps
COPY pyproject.toml /app/
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -e .

# App code
COPY src /app/src

EXPOSE 8080
CMD ["python", "-m", "src.serve"]
