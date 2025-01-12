// HeaderBar.js
import React from 'react';
import UserDropdown from './UserDropdown'; // Assuming you already have this component
import './HeaderBar.css'

const HeaderBar = ({ title, currentUser, onLogout, onNavigate }) => {
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
        currentUser={currentUser}
        onSettings={() => onNavigate('/user/settings')}
        onLogout={onLogout}
      />
    </div>
  );
};

export default HeaderBar;
