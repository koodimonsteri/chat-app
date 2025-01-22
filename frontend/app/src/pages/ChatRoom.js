import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import HeaderBar from '../components/HeaderBar';
import './ChatRoom.css'
import { fetchCurrentUser } from '../api';


const ChatRoom = ({ currentUser, onLogout }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [ws, setWs] = useState(null);
  const wsRef = useRef(null);
  const { chatId } = useParams();
  const location = useLocation();
  const [loading, setLoading] = useState(true);
  const [chat, setChat] = useState(location.state?.chat || null);
  const navigate = useNavigate();

  useEffect(() => {
    if (location.state?.chat) {
      setChat(location.state.chat);
    } else {
      // Fetch chat data or handle cases where it's not available
    }
    if (!currentUser) {
      currentUser = fetchCurrentUser()
    }
    if (currentUser && chat) {
      setLoading(false);
    }
  }, [location.state, currentUser, chatId, chat]);
  
  useEffect(() => {
    console.log(currentUser)
    console.log(chat)
    if (!currentUser || !chat) return;
    //const token = `Bearer ${localStorage.getItem('jwt_token')}`;
    const token = `${localStorage.getItem('jwt_token')}`;
    const socketUrl = `ws://localhost:8000/ws/chat/${chat.id}?token=${token}`;
    const socket = new WebSocket(socketUrl);

    socket.onopen = () => {
      //const joinMessage = {
      //  type: 'join',
      //  chatId: chat.id,
      //  userId: currentUser.id,
      //  token: token,
      //};
      //socket.send(JSON.stringify(joinMessage));
      console.log('Opened websocket!')
    };

    socket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages(prevMessages => [...prevMessages, message]);
    };

    socket.onclose = () => {
      console.log('WebSocket disconnected');
    };

    wsRef.current = socket;
    setWs(socket);

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [currentUser, chat]);

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      ws.send(JSON.stringify({ sender_username: currentUser.username, content: newMessage }));
      setNewMessage('');
    }
  };

  const handleNavigation = (path) => {
    if (wsRef.current) {
      wsRef.current.close();
    }
    navigate(path);
  };

  const handleLogoutClick = () => {
    if (wsRef.current) {
      wsRef.current.close();
    }
    onLogout();
  };
  
  return (
    <div className="chat-room">
      <HeaderBar
        title={chat.name || 'Chat Room'}
        currentUser={currentUser}
        onLogout={handleLogoutClick}
        onNavigate={handleNavigation}
      />
      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className="message">
            <strong>{message.sender_username}: </strong>{message.content}
          </div>
        ))}
      </div>

      <div className="chat-input">
        <textarea
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatRoom;
