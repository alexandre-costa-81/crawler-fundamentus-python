FROM python:3.11-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/cron.d/fundamentus-cron

RUN chmod 0644 /etc/cron.d/fundamentus-cron \
    && crontab /etc/cron.d/fundamentus-cron

CMD ["cron", "-f"]
