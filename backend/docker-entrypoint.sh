#!/bin/bash

# Check if the setup flag file exists inside the container (temporary file, not persisted via volumes)
if [ ! -f /tmp/.setup_done ]; then
    echo "Running initial setup..."

    # Check if JWT keys exist in /config/jwt; if not, generate them
    if [ ! -f "$JWT_SECRET_KEY_PATH" ]; then
        echo "JWT private and public keys not found. Generating..."

        mkdir -p /var/www/html/config/jwt
        
        openssl genpkey -out "$JWT_SECRET_KEY_PATH" -algorithm RSA -pkeyopt rsa_keygen_bits:4096
        openssl rsa -pubout -in "$JWT_SECRET_KEY_PATH" -out "$JWT_PUBLIC_KEY_PATH"
        chmod 644 "$JWT_SECRET_KEY_PATH"
        chmod 644 "$JWT_PUBLIC_KEY_PATH"
    
        echo "JWT keys generated successfully."
    fi

    if [ ! -f /var/www/html/config/ssl/private.key ]; then
        echo "SSL certificates not found. Generating..."

        mkdir -p /var/www/html/config/ssl
        
        openssl genpkey -algorithm RSA -out /var/www/html/config/ssl/private.key -pkeyopt rsa_keygen_bits:4096
        openssl req -new -key /var/www/html/config/ssl/private.key -out /var/www/html/config/ssl/certificate.csr -subj "/C=US/ST=California/L=San Francisco/O=MyApp/CN=localhost"
        openssl x509 -req -days 365 -in /var/www/html/config/ssl/certificate.csr -signkey /var/www/html/config/ssl/private.key -out /var/www/html/config/ssl/certificate.crt
        echo "SSL certificates generated successfully."
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