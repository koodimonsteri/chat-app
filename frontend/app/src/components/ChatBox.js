import React, { useState } from 'react';


const ChatBox = ({ friend, onSendMessage, messages, wsConnected }) => {
    const [message, setMessage] = useState("");
  
    const handleSend = (e) => {
      e.preventDefault();
      if (message.trim()) {
        onSendMessage(message);
        setMessage("");
      }
    };
  
    return (
      <div className="h-full flex flex-col">
        <div className="p-4 border-b border-gray-300">
          <h2 className="text-xl font-bold">{friend.username}</h2>
          <p className="text-sm text-gray-500">
            WebSocket: {wsConnected ? "Connected" : "Disconnected"}
          </p>
        </div>
        <div className="flex-grow overflow-y-auto p-4">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`mb-2 ${
                msg.self ? "text-right" : "text-left"
              }`}
            >
              <span
                className={`inline-block px-4 py-2 rounded-lg ${
                  msg.self
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200 text-black"
                }`}
              >
                {msg.content}
              </span>
            </div>
          ))}
        </div>
        <form
          onSubmit={handleSend}
          className="border-t border-gray-300 p-4 flex items-center"
        >
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="flex-grow border rounded p-2"
            placeholder="Type a message..."
          />
          <button
            type="submit"
            className="ml-2 bg-blue-500 text-white px-4 py-2 rounded"
          >
            Send
          </button>
        </form>
      </div>
    );
  };
  
  export default ChatBox;
  