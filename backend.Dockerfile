FROM python:3.12-slim

LABEL maintainer="mihai@developerakademie.com"
LABEL version="1.0"
LABEL description="Python 3.14.0a7 Alpine 3.21"

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        postgresql-client \
        ffmpeg \
        build-essential \
        gcc \
        libpq-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    chmod +x backend.entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "./backend.entrypoint.sh" ]
