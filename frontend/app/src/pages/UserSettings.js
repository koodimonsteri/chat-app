import React, { useState, useEffect } from 'react';
import UserDropdown from '../components/UserDropdown';
import './UserSettings.css';
import { fetchCurrentUser } from '../api';
import { useNavigate } from 'react-router-dom';
import Spinner from '../components/Spinner';

const UserSettings = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    let isMounted = true;

    const fetchUserData = async () => {
        try {
          const result = await fetchCurrentUser();
          if (isMounted) {
            setUserData(result);
            setLoading(false);
          }
        } catch (err) {
          if (isMounted) {
            setError('Failed to load user data');
            setLoading(false);
          }
        }
      };
      fetchUserData()

    return () => {
      isMounted = false;
    };
  }, []);

  const handleGoToDashboard = () => {
    navigate('/dashboard');
  };

  return (
    <div className="user-settings-page">
      <div className="user-settings-header">
        <h1>User Settings</h1>

        <div className="chat-dashboard-btn-container">
          <button className="chat-dashboard-btn" onClick={handleGoToDashboard}>
            Chat Dashboard
          </button>
        </div>

        <UserDropdown navigate={navigate} />
      </div>

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
