# Chat-App

Learning some php and symfony.\
Created REST API backend.\
Routes:\
/auth with /register and /login\
/chat to manage chats\
/user to manage users\
/websocket WIP

React frontend to register/login\
Dashboard to manage chats\
Chat rooms to chat with other users WIP


Project is set up so that you can just build it with docker.\
rename .env.example to .env in project root\
rename .env.dev to .env in backend/app\
docker-compose up --build -d

then you can start server\
docker-compose exec backend php -S 0.0.0.0:8000 -t public\
API can be accessed in http://localhost:8000 \
frontend can be accessed in http://localhost:3000

Login page:\
![loginpage](https://github.com/user-attachments/assets/c1f28b05-c5e8-417f-9b5d-d7911d3b5f0c)

Register page:\
![registerpage](https://github.com/user-attachments/assets/3d7768c6-c65c-47a5-8fd1-5af389ab54ba)

Create chats:\
![create chats](https://github.com/user-attachments/assets/c3cfe5c9-ae49-4329-ad15-1835981573e3)

Public chats:\
![public chats](https://github.com/user-attachments/assets/4be3e908-cb49-4973-ab08-1bd38aec0819)

My chats:\
![my chats](https://github.com/user-attachments/assets/9c0ad307-13df-425d-907f-b634f2a51073)

Chatrooms:\
![chatroom](https://github.com/user-attachments/assets/e4c4c696-1501-4c66-9b0d-375ad94b397b)

User settings:\
![user settings](https://github.com/user-attachments/assets/14f52b2f-46fb-4322-a144-21b3a4ddeee1)
