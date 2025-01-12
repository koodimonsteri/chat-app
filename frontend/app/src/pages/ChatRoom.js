import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import HeaderBar from '../components/HeaderBar';
import './ChatRoom.css'


const ChatRoom = ({ currentUser, onLogout }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [ws, setWs] = useState(null);
  const wsRef = useRef(null);
  const { chatId } = useParams();
  const location = useLocation();
  const [chat, setChat] = useState(location.state?.chat || null);
  const navigate = useNavigate();

  useEffect(() => {
    if (location.state?.chat){
      console.log('set chat')
      setChat(location.state.chat)
    } else {
      //TODO fetch
    }
    const token = `Bearer ${localStorage.getItem('jwt_token')}`
    //const socket = new WebSocket(`ws://localhost:8080/chat/${chatId}/connect?token=${token}`);
    const socket = new WebSocket(`ws://localhost:9090`);

    socket.onopen = () => {
      console.log('WebSocket connected');
      socket.send(JSON.stringify({ type: 'join', chatId: chat.id, userId: currentUser.id }));
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
  }, [location.state, chatId, currentUser]);

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      ws.send(JSON.stringify({ type: 'message', content: newMessage }));
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
            <strong>{message.user}: </strong>{message.content}
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
