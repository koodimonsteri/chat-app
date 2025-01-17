import React, { useState, useEffect } from 'react';
import HeaderBar from '../components/HeaderBar';
import './UserSettings.css';
import { fetchCurrentUser, updateUser } from '../api';
import { useNavigate } from 'react-router-dom';
//import Spinner from '../components/Spinner';

const UserSettings = ({ currentUser, onLogout }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    //username: currentUser.username,
    email: currentUser.email,
    description: currentUser.description,
  });
  const [originalData, setOriginalData] = useState({
    //username: currentUser.username,
    email: currentUser.email,
    description: currentUser.description,
  });
  const [message, setMessage] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const getChangedFields = () => {
    const changedFields = {};
    Object.keys(formData).forEach((key) => {
      if (formData[key] !== originalData[key]) {
        changedFields[key] = formData[key];
      }
    });
    return changedFields;
  };

  const handleUpdate = async () => {
    const changedData = getChangedFields();
    
    if (Object.keys(changedData).length === 0) {
      setMessage({ type: 'info', text: 'No changes made.' });
      return;
    }
    console.log("changed data", changedData)
    try {
      await updateUser(currentUser.id, changedData);
      setMessage({ type: 'success', text: 'User updated successfully!' });
      setOriginalData(formData);
    } catch (error) {
      setMessage({ type: 'error', text: 'Error updating user data' });
    }
  };

  const handleRefresh = async () => {
    try {
      const refreshedUserData = await fetchCurrentUser();  // This fetches the latest user data from the backend
      setFormData({
        username: refreshedUserData.username,
        email: refreshedUserData.email,
        description: refreshedUserData.description,
      });
      setOriginalData({
        username: refreshedUserData.username,
        email: refreshedUserData.email,
        description: refreshedUserData.description,
      });
      setMessage(null)
    } catch (error) {
      console.error("Error refreshing user data:", error);
      setMessage({ type: 'error', text: 'Error refreshing user data' });
    }
  };

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
        {message && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}

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
              <div className="label">ID:</div>
              <div className="value">{currentUser.username}</div>
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
