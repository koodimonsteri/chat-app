import React, { useState, useEffect } from 'react';
import HeaderBar from '../components/HeaderBar';
import './UserSettings.css';
import { fetchCurrentUser } from '../api';
import { useNavigate } from 'react-router-dom';
import Spinner from '../components/Spinner';

const UserSettings = ({ currentUser, onLogout }) => {

  const navigate = useNavigate();

  console.log(currentUser)
  const handleGoToDashboard = () => {
    navigate('/dashboard');
  };

  const handleNavigation = async (path) => {
    navigate(path);
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

          {! currentUser && <div className="error">Error loading user data</div>}

          { currentUser && (
            <>
              <div className="user-info-row">
                <div className="label">ID:</div>
                <div className="value">{currentUser.id}</div>
                <div className="button-container"></div>
              </div>
              <div className="user-info-row">
                <div className="label">Username:</div>
                <div className="value">{currentUser.username}</div>
                <div className="button-container">
                  <button onClick={() => alert('Update username')}>Update</button>
                </div>
              </div>
              <div className="user-info-row">
                <div className="label">Email:</div>
                <div className="value">{currentUser.email}</div>
                <div className="button-container">
                  <button onClick={() => alert('Update email')}>Update</button>
                </div>
              </div>
              <div className="user-info-row">
                <div className="label">Description:</div>
                <div className="value">{currentUser.description}</div>
                <div className="button-container">
                  <button onClick={() => alert('Update email')}>Update</button>
                </div>
              </div>
              <div className="user-info-row">
                <div className="label">Created At:</div>
                <div className="value">{new Date(currentUser.created_at).toLocaleString()}</div>
                <div className="button-container"></div>
              </div>
              <div className="user-info-row">
                <div className="label">Updated At:</div>
                <div className="value">{new Date(currentUser.updated_at).toLocaleString()}</div>
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
