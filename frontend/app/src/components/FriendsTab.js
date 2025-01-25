import React, { useState, useEffect } from "react";
import ChatBox from "./ChatBox";
import "./FriendsTab.css";

const FriendsTab = () => {
  const [friends, setFriends] = useState([]);
  const [friendRequests, setFriendRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedFriend, setSelectedFriend] = useState(null);
  const [newFriendEmail, setNewFriendEmail] = useState("");

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
    if (!newFriendEmail.trim()) return;

    try {
      const response = await fetch("/api/user/friend-requests", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: newFriendEmail }),
      });

      if (!response.ok) {
        throw new Error("Failed to send friend request");
      }

      setNewFriendEmail("");
      alert("Friend request sent!");
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
            value={newFriendEmail}
            onChange={(e) => setNewFriendEmail(e.target.value)}
            placeholder="Enter email to add friend"
          />
          <button onClick={handleAddFriend}>Add</button>
        </div>

        <div className="expandable-section">
          <button onClick={toggleFriendRequests}>
            Friend Requests ({friendRequests.length})
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
