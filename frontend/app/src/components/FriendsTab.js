import React, { useState, useEffect } from "react";
import ChatBox from "./ChatBox";
import "./FriendsTab.css";
import { useUser } from '../context/UserContext';
import { postFriendRequest, getFriendRequests, getFriends, acceptFriendRequest } from '../api.js'

const FriendsTab = () => {
  const { currentUser } = useUser();
  const [friends, setFriends] = useState([]);
  const [sentRequests, setSentRequests] = useState([]);
  const [receivedRequests, setReceivedRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedFriend, setSelectedFriend] = useState(null);
  const [newFriendUsername, setNewFriendUsername] = useState("");

  const [showSentRequests, setShowSentRequests] = useState(false);
  const [showReceivedRequests, setShowReceivedRequests] = useState(false);
  const [showFriends, setShowFriends] = useState(true);

  const [messages, setMessages] = useState([]);
  const [wsConnected, setWsConnected] = useState(false);
  const [socket, setSocket] = useState(null);


  const fetchData = async () => {
    try {
      console.log('Starting fetch data')
      const [friendsResponse, requestsResponse] = await Promise.allSettled([
      getFriends(currentUser.id).catch((err) => {
          console.error("Error fetching friends:", err);
          throw err;
          }),
      getFriendRequests(currentUser.id).catch((err) => {
          console.error("Error fetching friend requests:", err);
          throw err;
          }),
      ]);
      if (!friendsResponse.ok || !requestsResponse.ok) {
        setError('Failed to fetch friends.');
      }

      const friendRequests = requestsResponse.data.friend_requests;
      const sent = friendRequests.filter(request => request.sender_id === currentUser.id);
      const received = friendRequests.filter(request => request.receiver_id === currentUser.id);
      console.log('Friends: %s', friendsResponse)
      setFriends(friendsResponse.data);
      setSentRequests(sent);
      setReceivedRequests(received); 
      setLoading(false);
    } catch (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();

  }, []);

  const handleAddFriend = async () => {
    if (!newFriendUsername.trim()) return;

    try {
        const result = await postFriendRequest(currentUser.id, newFriendUsername);
    
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

  const toggleSentRequests = () => {
    setShowSentRequests((prev) => !prev);
  };

  const toggleReceivedRequests = () => {
    setShowReceivedRequests((prev) => !prev);
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

  const handleAcceptFriend = async (request_id) => {
    try {
      const accepted = await acceptFriendRequest(currentUser.id, request_id);
  
      if (accepted.success) {
        await fetchData();
        alert("Friend request accepted!");
      } else {
        alert("Failed to accept friend request");
      }
    } catch (error) {
      console.error("Error accepting friend request:", error);
      alert("Something went wrong. Please try again.");
    }
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
          <button onClick={toggleSentRequests}>
            Sent Requests ({sentRequests.length})
          </button>
          {showSentRequests && (
            <ul>
              {sentRequests.map((request) => (
                <li key={request.guid} className="request-item">
                  <span>{request.receiver.username}</span>
                  <button onClick={() => alert("Reject logic here!")}>
                    Reject
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="expandable-section">
          <button onClick={toggleReceivedRequests}>
            Received Requests ({receivedRequests.length})
          </button>
          {showReceivedRequests && (
            <ul>
              {receivedRequests.map((request) => (
                <li key={request.guid} className="request-item">
                  <span>{request.sender.username}</span>
                  <button onClick={() => handleAcceptFriend(request.id)}>
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
