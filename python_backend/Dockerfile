FROM python:3.9-slim

EXPOSE 8000

# Netcat for checking if database is ready
# Openssl to generate some keys
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    openssl

# Copy alembic stuff for migrations
COPY /chat_db_migrations ./chat_db_migrations

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /app .

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT [ "docker-entrypoint.sh" ]