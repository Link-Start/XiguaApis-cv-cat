FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN python --version && node --version && npm --version

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser && chown -R appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production

CMD ["python", "watermelon_api.py"]
