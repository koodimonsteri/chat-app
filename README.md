# Chat-App

Learning some php and symfony.\
Created REST API backend.\
Routes:\
/auth with /register and /login\
/chat to manage chats\
/user to manage users

React frontend to register/login\
Dashboard to manage chats WIP

Project is set up so that you can just build it with docker.\
rename .env.example to .env in project root\
rename .env.dev to .env in backend/app\
docker-compose up --build -d

then you can start server\
docker-compose exec backend php -S 0.0.0.0:8000 -t public\
API can be accessed in http://localhost:8000 \
frontend can be accessed in http://localhost:3000
