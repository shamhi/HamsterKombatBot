FROM python:3.11.9-slim as builder
LABEL org.opencontainers.image.source=https://github.com/shamhi/HamsterKombatBot
WORKDIR /app

COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps

FROM python:3.11.9-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
