// src/api.js

const apiUrl = process.env.REACT_APP_API_URL;

const getAuthHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem('jwt_token')}`,
  'Content-Type': 'application/json',
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

export const updateUser = async (userId, userData) => {
  const response = await fetch(`${apiUrl}/api/user/${userId}`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    throw new Error('Failed to update user data');
  }

  return await response.json();
}

export const sendFriendRequest = async (user_id, username) => {
  const apiUrl = `${apiUrl}/api/user/${user_id}/friends/request`;

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to send friend request");
    }

    return { success: true, message: "Friend request sent!" };
  } catch (error) {
    return { success: false, message: error.message };
  }
};