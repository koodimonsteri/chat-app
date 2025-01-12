#!/bin/bash

# Check if the setup flag file exists inside the container (temporary file, not persisted via volumes)
if [ ! -f /tmp/.setup_done ]; then
    echo "Running initial setup..."

    # Check if JWT keys exist in /config/jwt; if not, generate them
    if [ ! -f /var/www/html/config/jwt/private.key ]; then
        echo "JWT private and public keys not found. Generating..."
        mkdir -p /var/www/html/config/jwt
        openssl genpkey -out /var/www/html/config/jwt/private.pem -algorithm RSA -pkeyopt rsa_keygen_bits:4096
        openssl rsa -pubout -in /var/www/html/config/jwt/private.pem -out /var/www/html/config/jwt/public.pem
        echo "JWT keys generated successfully."
    fi

    echo "Waiting for MySQL to be ready..."
    echo "$DB_HOST"
    echo "$DB_USER"
    echo "$DB_PASSWORD"
    echo "$DB_ROOT_PASSWORD"
    until nc -z -v -w30 "$DB_HOST" 3306; do
        echo "Waiting for MySQL to be available..."
        sleep 10
    done
    echo "MySQL is ready!"

    echo "Creating database with Doctrine..."
    php bin/console doctrine:database:create --if-not-exists --env=$APP_ENV

    echo "Running Symfony migrations..."
    php bin/console doctrine:migrations:migrate --no-interaction

    touch /tmp/.setup_done
    echo "Initial setup completed."

else
    echo "Setup already completed. Skipping initial setup."
fi

echo "Clearing cache..."
php bin/console cache:clear --env=$APP_ENV

#exec "$@"
php-fpm # &
#php /var/www/html/bin/console app:websocket-server