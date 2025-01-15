import React, { useState, useEffect } from 'react';
import HeaderBar from '../components/HeaderBar';
import './UserSettings.css';
import { fetchCurrentUser } from '../api';
import { useNavigate } from 'react-router-dom';
import Spinner from '../components/Spinner';

const UserSettings = ({ currentUser, onLogout }) => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleGoToDashboard = () => {
    navigate('/dashboard');
  };


  const handleNavigation = (path) => {
    navigate(path);  // Navigate to the given path
  };

  return (
    <div className="user-settings-page">
      <HeaderBar
        title="User Settings"
        currentUser={currentUser}
        onSettings={() => {}}
        onLogout={onLogout}
        onDashboard={handleGoToDashboard}
        onClose={() => {}}
        onNavigate={handleNavigation}
      />

      <div className="user-settings-content">
        <div className="user-info">
          {loading && (
            <div className="loading-container">
              <span>Loading user data...</span>
              <Spinner />
            </div>
          )}
          {error && <div>Error loading user data: {error}</div>}

          {!loading && !error && (
            <>
              <div className="user-info-row">
                <div className="label">ID:</div>
                <div className="value">{userData.id}</div>
                <div className="button-container"></div>
              </div>
              <div className="user-info-row">
                <div className="label">Username:</div>
                <div className="value">{userData.username}</div>
                <div className="button-container">
                  <button onClick={() => alert('Update username')}>Update</button>
                </div>
              </div>
              <div className="user-info-row">
                <div className="label">Email:</div>
                <div className="value">{userData.email}</div>
                <div className="button-container">
                  <button onClick={() => alert('Update email')}>Update</button>
                </div>
              </div>
              <div className="user-info-row">
                <div className="label">Created At:</div>
                <div className="value">{new Date(userData.created_at).toLocaleString()}</div>
                <div className="button-container"></div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserSettings;
