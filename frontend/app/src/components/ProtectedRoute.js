import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode'; // Ensure correct import path
import { fetchCurrentUser } from '../api'; // Your API call for fetching the current user
import Spinner from './Spinner';

const ProtectedRoute = ({ element: Component, ...rest }) => {
  const token = localStorage.getItem('jwt_token');
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    try {
      //const decoded = jwtDecode(token);

      const fetchUser = async () => {
        try {
          const user = await fetchCurrentUser();
          setCurrentUser(user);
        } catch (err) {
          console.error('Error fetching user:', err);
          localStorage.removeItem('jwt_token');
        } finally {
          setLoading(false);
        }
      };

      fetchUser();
    } catch (err) {
      console.error('Invalid JWT:', err);
      localStorage.removeItem('jwt_token');
      setLoading(false);
    }
  }, [token]);

  if (loading) {
    return <Spinner />;
  }

  if (!currentUser) {
    return <Navigate to="/" />;
  }

  return <Component {...rest} currentUser={currentUser} />;
};

export default ProtectedRoute;
