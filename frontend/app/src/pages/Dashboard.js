import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import './Dashboard.css';
import Spinner from '../components/Spinner';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('myChats'); // Default tab is "My Chats"
  const [createChatFormData, setCreateChatFormData] = useState({
    name: '',
    is_private: true,
  });
  const [createChatFormError, setCreateChatFormError] = useState('');
  const [createChatFormSuccess, setCreateChatFormSuccess] = useState('');
  
  const [myChats, setMyChats] = useState([]);
  const [loadingChats, setLoadingChats] = useState(false);
  const [myChatsError, setMyChatsError] = useState('');
  const [expandedChat, setExpandedChat] = useState(null);

  const [publicChats, setPublicChats] = useState([]);
  const [loadingPublicChats, setLoadingPublicChats] = useState(false);
  const [publicChatError, setPublicChatError] = useState('');

  const [currentUser, setCurrentUser] = useState(null); // Stores current user info
  const [loadingUser, setLoadingUser] = useState(true);

  const navigate = useNavigate();

  const apiUrl = process.env.REACT_APP_API_URL;

  const handleCreateFormInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setCreateChatFormData({
      ...createChatFormData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const fetchCurrentUser = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/user/current`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('jwt_token')}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to fetch current user');
      }
      const userData = await response.json();
      setCurrentUser(userData);
    } catch (error) {
      console.error('Error fetching current user:', error);
    } finally {
      setLoadingUser(false);
    }
  };
  useEffect(() => {
    fetchCurrentUser();
  }, []);

  const handleCreateFormSubmit = async (e) => {
    e.preventDefault();
    setCreateChatFormError('');
    setCreateChatFormSuccess('');
    try {
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('jwt_token')}`,
        },
        body: JSON.stringify(createChatFormData),
      });
      if (!response.ok) {
        throw new Error('Failed to create chat');
      }
      setCreateChatFormSuccess('Chat created successfully!');
      setCreateChatFormData({ name: '', is_private: true });
      //setActiveTab('myChats')
    } catch (error) {
      setCreateChatFormError(error.message || 'An error occurred');
    }
  };

  const toggleChatExpand = (chatId) => {
    setExpandedChat((prev) => (prev === chatId ? null : chatId));
  };

  const fetchMyChats = async () => {
    setLoadingChats(true);
    setMyChatsError('');
    try {
      const response = await fetch(`${apiUrl}/api/chat/user`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('jwt_token')}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to fetch chats');
      }
      const data = await response.json();
      setMyChats(data);
    } catch (error) {
      setMyChatsError(error.message || 'An error occurred');
    } finally {
      setLoadingChats(false);
    }
  };

  const fetchPublicChats = async () => {
    setLoadingPublicChats(true);
    setPublicChatError('');
    try {
      const response = await fetch(`${apiUrl}/api/chat`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('jwt_token')}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to fetch public chats');
      }
      const data = await response.json();
      setPublicChats(data);
    } catch (error) {
      setPublicChatError(error.message || 'An error occurred');
    } finally {
      setLoadingPublicChats(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'myChats') {
      fetchMyChats();
    } else if (activeTab === 'public') {
      fetchPublicChats();
    }
  }, [activeTab]);

  const renderContent = () => {
    switch (activeTab) {
      case 'create':
        return (
          <form className="create-chat-form" onSubmit={handleCreateFormSubmit}>
            <div className="form-group">
              <label htmlFor="name">Chat Name:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={createChatFormData.name}
                onChange={handleCreateFormInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="is_private">Private:</label>
              <input
                type="checkbox"
                id="is_private"
                name="is_private"
                checked={createChatFormData.is_private}
                onChange={handleCreateFormInputChange}
              />
            </div>
            <button type="submit" className="submit-button">Create Chat</button>
            {createChatFormError && <p className="error-message">{createChatFormError}</p>}
            {createChatFormSuccess && <p className="success-message">{createChatFormSuccess}</p>}
          </form>
        );
      case 'public':
        return (
          <div className="public-chats-list">
            {loadingPublicChats ? (
              <Spinner />
            ) : publicChatError ? (
              <p className="error-message">{publicChatError}</p>
            ) : publicChats.length > 0 ? (
              <ul>
                {publicChats.map((chat) => (
                  <li key={chat.id}>
                    <p><strong>{chat.name}</strong></p>
                    <p>{chat.is_private ? 'Private' : 'Public'}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No public chats found.</p>
            )}
          </div>
        );
      case 'myChats':
        return (
          <div className="my-chats-list">
            {loadingChats ? (
              <Spinner />
            ) : myChatsError ? (
              <p className="error-message">{myChatsError}</p>
            ) : myChats.length > 0 ? (
              <ul>
                {myChats.map((chat) => (
                  <li key={chat.id} className="chat-item">
                    <div
                      className="chat-summary"
                      onClick={() => toggleChatExpand(chat.id)}
                    >
                      <p><strong>{chat.name}</strong></p>
                      <p>{chat.is_private ? 'Private' : 'Public'}</p>
                    </div>
                    {expandedChat === chat.id && (
                      <div className="chat-details">
                        <p><strong>Owner:</strong> {chat.chat_owner.username}</p>
                        <p><strong>Created At:</strong> {new Date(chat.created_at).toLocaleString()}</p>
                        <div className="chat-actions">
                          <button className="join-button">Join</button>
                          {currentUser?.username === chat.chat_owner.username && (
                            <button className="invite-button">Invite</button>
                          )}
                        </div>
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No chats found.</p>
            )}
          </div>
        );
      default:
        return <div>Select an option above</div>;
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('jwt_token');
    navigate('/');
  };

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <h1>Chat Dashboard</h1>
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>
      <div className="dashboard-nav">
        <button
          className={activeTab === 'create' ? 'active' : ''}
          onClick={() => setActiveTab('create')}
        >
          Create Chat
        </button>
        <button
          className={activeTab === 'public' ? 'active' : ''}
          onClick={() => setActiveTab('public')}
        >
          Public Chats
        </button>
        <button
          className={activeTab === 'myChats' ? 'active' : ''}
          onClick={() => setActiveTab('myChats')}
        >
          My Chats
        </button>
      </div>
      <div className="dashboard-content">{renderContent()}</div>
    </div>
  );
};

export default Dashboard;