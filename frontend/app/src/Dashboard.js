import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import './Dashboard.css';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('myChats'); // Default tab is "My Chats"
  const navigate = useNavigate();

  const renderContent = () => {
    switch (activeTab) {
      case 'create':
        return <div>Create Chat Form</div>;
      case 'public':
        return <div>Public Chats List</div>;
      case 'invite':
        return <div>Invite User Form</div>;
      case 'myChats':
        return <div>My Chats List</div>;
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
          className={activeTab === 'invite' ? 'active' : ''}
          onClick={() => setActiveTab('invite')}
        >
          Invite
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