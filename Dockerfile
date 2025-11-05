# Base image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (optional): uncomment if needed for geospatial stack later
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md /app/
COPY src /app/src
COPY requirements.txt /app/requirements.txt

# Install in editable mode for development (or use regular install)
RUN pip install --upgrade pip && pip install -e .

EXPOSE 8000
CMD ["uvicorn", "a2aworld.a2a_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
