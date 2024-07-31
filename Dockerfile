FROM python:3.11.9-slim as builder
LABEL org.opencontainers.image.source=https://github.com/shamhi/HamsterKombatBot
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libssl-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

FROM python:3.11.9-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

RUN python -m playwright install --with-deps chromium && \
    rm -rf /var/lib/apt/lists/*

COPY . .
