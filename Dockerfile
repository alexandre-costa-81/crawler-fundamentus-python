FROM python:3.11-slim

RUN apt-get update && apt-get install -y cron tzdata

ENV TZ="America/Sao_Paulo"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/cron.d/fundamentus-cron

RUN chmod 0644 /etc/cron.d/fundamentus-cron \
    && crontab /etc/cron.d/fundamentus-cron

CMD ["cron", "-f"]
