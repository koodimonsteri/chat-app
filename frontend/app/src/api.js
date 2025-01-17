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
  try {
    const response = await fetch(`${apiUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify(chatData),
    });
    if (!response.ok) {
      if (response.status === 401) {
        return { error: 'JWT expired' };
      }
      throw new Error('Failed to create chat');
    }
    return await response.json();
  } catch (error) {
    console.error('Error creating chat:', error);
    return { error: error.message };
  }
};

export const fetchMyChats = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/chat/user`, {
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


export const apiLogin = async (username, password) => {
  try {
    const response = await fetch(`${apiUrl}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username,
      password,
      }),
    });
  } catch (error) {
    console.log("error", error)
  };
};