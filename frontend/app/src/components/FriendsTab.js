import React, { useState, useEffect } from "react";
import ChatBox from "./ChatBox";
import "./FriendsTab.css";
import { useUser } from '../context/UserContext';
import { sendFriendRequest } from '../api.js'

const FriendsTab = () => {
  const { currentUser } = useUser();
  const [friends, setFriends] = useState([]);
  const [friendRequests, setFriendRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedFriend, setSelectedFriend] = useState(null);
  const [newFriendUsername, setNewFriendUsername] = useState("");

  const [showFriendRequests, setShowFriendRequests] = useState(false);
  const [showFriends, setShowFriends] = useState(true);

  const [messages, setMessages] = useState([]);
  const [wsConnected, setWsConnected] = useState(false);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [friendsResponse, requestsResponse] = await Promise.all([
          fetch("/api/user/friends"),
          fetch("/api/user/friend-requests"),
        ]);

        if (!friendsResponse.ok || !requestsResponse.ok) {
          throw new Error("Failed to fetch data");
        }

        const friendsData = await friendsResponse.json();
        const requestsData = await requestsResponse.json();

        setFriends(friendsData);
        setFriendRequests(requestsData);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleAddFriend = async () => {
    if (!newFriendUsername.trim()) return;

    try {
        const result = await sendFriendRequest(currentUser.id, newFriendUsername);
    
        if (result.success) {
          setNewFriendUsername("");
          alert(result.message);
        } else {
          alert(result.message);
        }
      } catch (error) {
        alert(error.message);
      }
  };

  const toggleFriendRequests = () => {
    setShowFriendRequests((prev) => !prev);
  };

  const toggleFriends = () => {
    setShowFriends((prev) => !prev);
  };

  const handleFriendClick = (friend) => {
    setSelectedFriend(friend);
    if (socket) socket.close();

    const newSocket = new WebSocket(`ws://localhost:8000/ws/user/${friend.guid}`);
    newSocket.onopen = () => {
      setWsConnected(true);
    };
    newSocket.onmessage = (event) => {
      const newMessage = JSON.parse(event.data);
      setMessages((prev) => [...prev, newMessage]);
    };
    newSocket.onclose = () => {
      setWsConnected(false);
    };
    setSocket(newSocket);
    setMessages([]);
  };

  return (
    <div className="flex h-full">
      <div className="sidebar">
        <div className="input-container">
          <input
            type="text"
            value={newFriendUsername}
            onChange={(e) => setNewFriendUsername(e.target.value)}
            placeholder="Enter username"
          />
          <button onClick={handleAddFriend}>Add</button>
        </div>

        <div className="expandable-section">
          <button onClick={toggleFriendRequests}>
            Sent Requests ({friendRequests.length})
          </button>
          {showFriendRequests && (
            <ul>
              {friendRequests.map((request) => (
                <li key={request.guid}>
                  <span>{request.username}</span>
                  <button onClick={() => alert("Accept logic here!")}>
                    Accept
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="expandable-section">
          <button onClick={toggleFriendRequests}>
            Received Requests ({friendRequests.length})
          </button>
          {showFriendRequests && (
            <ul>
              {friendRequests.map((request) => (
                <li key={request.guid}>
                  <span>{request.username}</span>
                  <button onClick={() => alert("Accept logic here!")}>
                    Accept
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="expandable-section">
          <button onClick={toggleFriends}>
            Friends ({friends.length})
          </button>
          {showFriends && (
            <ul>
              {friends.map((friend) => (
                <li key={friend.guid} onClick={() => handleFriendClick(friend)}>
                  {friend.username}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className="chat-box">
        {selectedFriend ? (
          <ChatBox
            friend={selectedFriend}
            onSendMessage={(message) => {
              socket.send(JSON.stringify({ message }));
              setMessages((prev) => [...prev, { self: true, content: message }]);
            }}
            messages={messages}
            wsConnected={wsConnected}
          />
        ) : (
          <div className="chat-box-placeholder">
            Select a friend to start chatting
          </div>
        )}
      </div>
    </div>
  );
};

export default FriendsTab;
