FROM python:3.12.11
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (better Docker caching)
COPY requirements.txt pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code
COPY . .

# Install backend as a package
RUN pip install -e .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1