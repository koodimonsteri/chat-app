import React, { useState, useEffect } from 'react';
import HeaderBar from '../components/HeaderBar';
import './UserSettings.css';
import { updateUser } from '../api';
import { useNavigate } from 'react-router-dom';
import Spinner from '../components/Spinner';

const UserSettings = ({ currentUser, onLogout }) => {
  const [formData, setFormData] = useState({
    username: currentUser.username,
    email: currentUser.email,
    description: currentUser.description,
  });
  const [originalData, setOriginalData] = useState({
    username: currentUser.username,
    email: currentUser.email,
    description: currentUser.description,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleUpdate = async () => {
    try {
      await updateUser(formData);
      alert('User updated successfully!');
      setOriginalData(formData);
    } catch (error) {
      alert('Error updating user data');
    }
  };

  const handleRefresh = () => {
    setFormData(originalData);
  };

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

          {currentUser && (
          <>
            <div className="user-info-row">
              <div className="label">ID:</div>
              <div className="value">{currentUser.id}</div>
              <div></div>
            </div>

            <div className="user-info-row">
              <div className="label">Username:</div>
              <div className="value">
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                />
              </div>
              <div></div>
            </div>

            <div className="user-info-row">
              <div className="label">Email:</div>
              <div className="value">
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                />
              </div>
              <div></div>
            </div>

            <div className="user-info-row">
              <div className="label">Description:</div>
              <div className="value">
                <input
                  type="text"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                />
              </div>
              <div></div>
            </div>

            <div className="user-info-row">
              <div className="label">Created At:</div>
              <div className="value">{new Date(currentUser.created_at).toLocaleString()}</div>
              <div></div>
            </div>

            <div className="user-info-row">
              <div className="label">Updated At:</div>
              <div className="value">{new Date(currentUser.updated_at).toLocaleString()}</div>
              <div></div>
            </div>


          </>
        )}
        </div>
        <div className="button-container">
              <button onClick={handleUpdate}>Update</button>
              <button onClick={handleRefresh}>Refresh</button>
            </div>
      </div>
    </div>
  );
};

export default UserSettings;
