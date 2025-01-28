import React, { useState, useEffect } from 'react';
import HeaderBar from '../components/HeaderBar';
import './UserSettings.css';
import { fetchCurrentUser, updateUser } from '../api';
import { useNavigate } from 'react-router-dom';
//import Spinner from '../components/Spinner';
import { useUser } from '../context/UserContext';

const UserSettings = ({ onLogout }) => {
  const { currentUser } = useUser();
  const [isOpenAITokenVisible, setIsOpenAITokenVisible] = useState(false);
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    //username: currentUser.username,
    email: currentUser.email,
    description: currentUser.description,
    openai_token: currentUser.openai_token
  });
  const [originalData, setOriginalData] = useState({
    //username: currentUser.username,
    email: currentUser.email,
    description: currentUser.description,
    openai_token: currentUser.openai_token
  });
  const [message, setMessage] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const getChangedFields = () => {
    const changedFields = {};
    Object.keys(formData).forEach((key) => {
      console.log(key)
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
      const updated_user = await updateUser(currentUser.id, changedData);
      setMessage({ type: 'success', text: 'User updated successfully!' });
      console.log('Updated user:', updated_user)
      setFormData({
        email: updated_user.email,
        description: updated_user.description,
        openai_token: updated_user.openai_token
      });
      setOriginalData({
        email: updated_user.email,
        description: updated_user.description,
        openai_token: updated_user.openai_token
      });
      
    } catch (error) {
      setMessage({ type: 'error', text: 'Error updating user data' });
    }
  };
  useEffect(() => {
    console.log('Updated originalData:', originalData);
  }, [originalData]);

  const handleRefresh = async () => {
    try {
      const refreshedUserData = await fetchCurrentUser();
      setFormData({
        username: refreshedUserData.username,
        email: refreshedUserData.email,
        description: refreshedUserData.description,
        openai_token: refreshedUserData.openai_token
      });
      setOriginalData({
        username: refreshedUserData.username,
        email: refreshedUserData.email,
        description: refreshedUserData.description,
        openai_token: refreshedUserData.openai_token
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
    setFormData(originalData)
    navigate(path);
  };

  const toggleTokenVisibility = () => {
    setIsOpenAITokenVisible(!isOpenAITokenVisible);
  };

  return (
    <div className="user-settings-page">
      <HeaderBar
        title="User Settings"
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
                <div className="label">OpenAI Token:</div>
                <div className="value">
                  {isOpenAITokenVisible ? (
                    <input
                      type="text"
                      name="openai_token"
                      value={formData.openai_token}
                      onChange={handleInputChange}
                    />
                  ) : (
                    <span>**********</span>
                  )}
                </div>
                <button onClick={toggleTokenVisibility}>
                  {isOpenAITokenVisible ? 'Hide Token' : 'Show Token'}
                </button>
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
