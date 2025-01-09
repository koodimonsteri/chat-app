# Chat-App

Learning some php and symfony.\
Created REST API backend.\
Implemented /register and /login\
Implemented /chat route to manage chats

Project is set up so that you can just build it with docker.\
rename .env.example to .env in project root\
rename .env.dev to .env in backend/app\
docker-compose up --build -d

then you can start server\
docker-compose exec backend php -S 0.0.0.0:8000 -t public\
API can be accessed in http://localhost:8000

Simple react frontend to register/login\
Simple dashboard to manage chats WIP\
frontend can be accessed in http://localhost:3000
