// src/api.js

const apiUrl = process.env.REACT_APP_API_URL;

const getAuthHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem('jwt_token')}`,
  'Content-Type': 'application/json',
});

export const fetchCurrentUser = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/users/me`, {
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
    return fetch(`${apiUrl}/api/chats`, {
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
    const response = await fetch(`${apiUrl}/api/chats?current_user=true`, {
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
    const response = await fetch(`${apiUrl}/api/chats`, {
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
  const response = await fetch(`${apiUrl}/api/users/${userId}`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    throw new Error('Failed to update user data');
  }

  return await response.json();
}

export const getFriends = async (user_id) => {
  const apiUrlWithParams = `${apiUrl}/api/users/${user_id}/friends`;

  try {
    const response = await fetch(apiUrlWithParams, {
      method: "GET",
      headers: getAuthHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to fetch friend requests");
    }

    const data = await response.json();
    return { success: true, data: data };
  } catch (error) {
    return { success: false, message: error.message };
  }
};

export const getFriendRequests = async (user_id) => {
  const apiUrlWithParams = `${apiUrl}/api/users/${user_id}/friend-requests`;

  try {
    const response = await fetch(apiUrlWithParams, {
      method: "GET",
      headers: getAuthHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to fetch friend requests");
    }

    const data = await response.json();
    return { success: true, data: data };
  } catch (error) {
    return { success: false, message: error.message };
  }
};

export const getFriendRequestById = async (user_id, request_id) => {
  const apiUrlWithParams = `${apiUrl}/api/users/${user_id}/friend-requests/${request_id}`;

  try {
    const response = await fetch(apiUrlWithParams, {
      method: "GET",
      headers: getAuthHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to fetch friend request details");
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, message: error.message };
  }
};

export const postFriendRequest = async (user_id, username) => {
  const apiUrlWithParams = `${apiUrl}/api/users/${user_id}/friend-requests`;

  try {
    const response = await fetch(apiUrlWithParams, {
      method: "POST",
      headers: getAuthHeaders(),
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

export const acceptFriendRequest = async (user_id, request_id) => {
  const apiUrlWithParams = `${apiUrl}/api/users/${user_id}/friend-requests/${request_id}/accept`;

  try {
    const response = await fetch(apiUrlWithParams, {
      method: "POST",
      headers: getAuthHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to accept friend request");
    }

    return { success: true, message: "Friend request accepted!" };
  } catch (error) {
    return { success: false, message: error.message };
  }
};

export const rejectFriendRequest = async (user_id, request_id) => {
  const apiUrlWithParams = `${apiUrl}/api/users/${user_id}/friend-requests/${request_id}/reject`;

  try {
    const response = await fetch(apiUrlWithParams, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ request_id }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to reject friend request");
    }

    return { success: true, message: "Friend request rejected!" };
  } catch (error) {
    return { success: false, message: error.message };
  }
};