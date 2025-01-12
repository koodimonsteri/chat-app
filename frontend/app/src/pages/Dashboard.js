import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

import './Dashboard.css';
import Spinner from '../components/Spinner';
import HeaderBar from '../components/HeaderBar';

import { fetchCurrentUser, createChat, fetchMyChats, fetchPublicChats } from '../api';

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

  const [currentUser, setCurrentUser] = useState(null);
  const [loadingUser, setLoadingUser] = useState(true);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);
  const userDropdownRef = useRef(null);
  const [currentPath, setCurrentPath] = useState(window.location.pathname);

  const navigate = useNavigate();

  const handleCreateFormInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setCreateChatFormData({
      ...createChatFormData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  useEffect(() => {
    const handleRouteChange = () => setCurrentPath(window.location.pathname);
    window.addEventListener('popstate', handleRouteChange);

    return () => {
      window.removeEventListener('popstate', handleRouteChange);
    };
  }, []);

  useEffect(() => {
    const fetchUserData = async () => {
      const result = await fetchCurrentUser();
      if (result.error === 'JWT expired') {
        localStorage.removeItem('jwt_token');
        navigate('/');
      } else {
        setCurrentUser(result);
      }
      setLoadingUser(false);
    };
    fetchUserData();
  }, [navigate]);

  const handleCreateFormSubmit = async (e) => {
    e.preventDefault();
    setCreateChatFormError('');
    setCreateChatFormSuccess('');
    try {
      const newChat = await createChat(createChatFormData);
      setCreateChatFormSuccess('Chat created successfully!');
      setCreateChatFormData({ name: '', is_private: true });
    } catch (error) {
      setCreateChatFormError(error.message || 'An error occurred');
    }
  };

  const toggleChatExpand = (chatId) => {
    setExpandedChat((prev) => (prev === chatId ? null : chatId));
  };

  const loadMyChatsData = async () => {
    setLoadingChats(true);
    const result = await fetchMyChats();
    if (result.error === 'JWT expired') {
      localStorage.removeItem('jwt_token');
      navigate('/');
    } else {
      setMyChats(result);
    }
    setLoadingChats(false);
  };

  const loadPublicChatsData = async () => {
    setLoadingPublicChats(true);
    const result = await fetchPublicChats();
    if (result.error === 'JWT expired') {
      localStorage.removeItem('jwt_token');
      navigate('/');
    } else {
      setPublicChats(result);
    }
    setLoadingPublicChats(false);
  };

  useEffect(() => {
    if (activeTab === 'myChats') {
      loadMyChatsData();
    } else if (activeTab === 'public') {
      loadPublicChatsData();
    }
  }, [activeTab]);

  //const handleOutsideClick = (event) => {
  //  if (userDropdownRef.current && !userDropdownRef.current.contains(event.target)) {
  //    setUserDropdownOpen(false);
  //  }
  //};

  const handleJoinChat = (chat) => {
    navigate(`/chat/${chat.id}`, { state: { chat } });  // Pass chat as state
  };

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
                          <button className="join-button" onClick={() => handleJoinChat(chat.id)}>
                            Join
                          </button>
                        </div>
                      </div>
                    )}
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
                          <button className="join-button" onClick={() => handleJoinChat(chat)}>
                            Join
                          </button>
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

  const handleNavigation = (path) => {
    navigate(path);  // Navigate to the given path
  };

  return (
    <div className="dashboard-page">
      <HeaderBar
        title="Dashboard"
        currentUser={currentUser}
        onLogout={handleLogout}
        onNavigate={handleNavigation}
      />
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