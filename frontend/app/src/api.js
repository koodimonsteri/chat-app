// src/api.js

const apiUrl = process.env.REACT_APP_API_URL;

const getAuthHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem('jwt_token')}`,
});

export const fetchCurrentUser = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/user/me`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Failed to fetch current user');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching current user:', error);
    return { error: error.message };
  }
};

export const createChat = async (chatData) => {
    return fetch(`${apiUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify(chatData),
    });
};

export const fetchMyChats = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/chat?current_user=true`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      if (response.status === 401) {
        return { error: 'JWT expired' };
      }
      throw new Error('Failed to fetch chats');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching my chats:', error);
    return { error: error.message };
  }
};

export const fetchPublicChats = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/chat`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      if (response.status === 401) {
        return { error: 'JWT expired' };
      }
      throw new Error('Failed to fetch public chats');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching public chats:', error);
    return { error: error.message };
  }
};

export const updateUser = async (userData) => {
  const response = await fetch('/api/user', {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('jwt')}`,
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    throw new Error('Failed to update user data');
  }

  return response.json();
}