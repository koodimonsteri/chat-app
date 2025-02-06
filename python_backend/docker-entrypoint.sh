#!/bin/bash
set -e

JWT_PRIVATE_KEY_PATH="$JWT_KEYS_DIR/private.pem"
JWT_PUBLIC_KEY_PATH="$JWT_KEYS_DIR/public.pem"

if [ ! -f /tmp/.setup_done ]; then
    echo "Running initial setup..."

    if [ ! -f "$JWT_PRIVATE_KEY_PATH" ] || [ ! -f "$JWT_PUBLIC_KEY_PATH" ]; then
        echo "JWT private and public keys not found. Generating..."

        mkdir -p "$JWT_KEYS_DIR"
        
        openssl genpkey -out "$JWT_PRIVATE_KEY_PATH" -algorithm RSA -pkeyopt rsa_keygen_bits:4096
        openssl rsa -pubout -in "$JWT_PRIVATE_KEY_PATH" -out "$JWT_PUBLIC_KEY_PATH"
        
        chmod 640 "$JWT_PRIVATE_KEY_PATH"
        chmod 644 "$JWT_PUBLIC_KEY_PATH"
        
        echo "JWT keys generated successfully."
    fi   

    echo $DB_HOST
    echo $DB_PORT
    echo "Waiting for PostgreSQL to be ready..."
    until nc -z -v -w30 "$DB_HOST" "$DB_PORT"; do
            echo "Waiting for PostgreSQL to be available..."
            sleep 5
    done
    echo "PostgreSQL is ready!"

    echo "Running Alembic migrations..."
    cd ../chat_db_migrations
    alembic upgrade head
    cd ..

    python ./app/prefill_db.py

    touch /tmp/.setup_done
fi

cd /app

exec "$@"