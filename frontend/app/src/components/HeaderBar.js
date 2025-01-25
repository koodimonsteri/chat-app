// HeaderBar.js
import React from 'react';
import UserDropdown from './UserDropdown';
import './HeaderBar.css'

const HeaderBar = ({ title, onLogout, onNavigate }) => {
    const handleGoToDashboard = () => {
        onNavigate('/dashboard');
      };

  return (
    <div className="header-bar">
      <h1>{title}</h1>
      
      <div className="chat-dashboard-btn-container">
          <button className="chat-dashboard-btn" onClick={handleGoToDashboard}>
          Chat Dashboard
          </button>
      </div>
      
      <UserDropdown
        onLogout={onLogout}
        onNavigate={onNavigate}
      />
    </div>
  );
};

export default HeaderBar;
