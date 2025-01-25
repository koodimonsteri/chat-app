import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import { fetchCurrentUser } from '../api';
import Spinner from './Spinner';

const ProtectedRoute = ({ element: Component, ...rest }) => {
  const { currentUser, setCurrentUser } = useUser();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('jwt_token');

    if (!token) {
      setLoading(false);
      return;
    }

    const fetchUser = async () => {
      try {
        const user = await fetchCurrentUser();
        setCurrentUser(user);
      } catch (error) {
        console.error('Error fetching user:', error);
        localStorage.removeItem('jwt_token');
      } finally {
        setLoading(false);
      }
    };

    if (!currentUser) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, [currentUser, setCurrentUser]);

  if (loading) {
    return <Spinner />;
  }

  if (!currentUser) {
    return <Navigate to="/login" />;
  }

  return <Component {...rest} />;
};

export default ProtectedRoute;
