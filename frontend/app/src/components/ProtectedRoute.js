import React from 'react';
import { jwtDecode } from 'jwt-decode';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ element: Component, currentUser, ...rest }) => {
  const token = localStorage.getItem('jwt_token');

  if (!token) {
    return <Navigate to="/" />;
  }

  try {
    const decoded = jwtDecode(token);
    const isTokenExpired = decoded.exp * 1000 < Date.now();

    if (isTokenExpired) {
      localStorage.removeItem('jwt_token');
      return <Navigate to="/" />;
    }
  } catch (error) {
    console.error('Invalid JWT:', error);
    localStorage.removeItem('jwt_token');
    return <Navigate to="/" />;
  }

  return <Component {...rest} currentUser={currentUser} />;
};

export default ProtectedRoute;
