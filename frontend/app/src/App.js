import { BrowserRouter as Router, Routes, Route, useNavigate, Navigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import UserSettings from './pages/UserSettings';
import ChatRoom from './pages/ChatRoom';
import { fetchCurrentUser } from './api';
import ProtectedRoute from './components/ProtectedRoute';
import { UserProvider } from './context/UserContext';

const App = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const navigate = useNavigate();
  
  const handleLogin = async (token) => {
    try {
      localStorage.setItem('jwt_token', token);
  
      const loadUser = await fetchCurrentUser();
      setCurrentUser(loadUser);
      navigate(`/dashboard`);
    } catch (error) {
      console.error("Error fetching the current user:", error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('jwt_token');
    navigate('/');
  };

  const handleSettings = async () => {
    const loadUser = await fetchCurrentUser();
    setCurrentUser(loadUser);
    navigate('/user/settings')
  };

  return (
    <UserProvider>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute
              element={ Dashboard }
              onSettings={handleSettings}
              onLogout={handleLogout} />} 
            />
        <Route 
          path="/user/settings"
          element={
            <ProtectedRoute
              element={ UserSettings }
              onLogout={handleLogout}
              />}
            />
        <Route 
          path="/chat/:chatId"
          element={
            <ProtectedRoute
              element={ ChatRoom } 
              onLogout={handleLogout}/>}
            />
      </Routes>
    </UserProvider>
  );
};

export default App;