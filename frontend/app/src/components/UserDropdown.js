import React, { useState, useEffect, useRef } from 'react';

import './UserDropdown.css';

const UserDropdown = React.forwardRef(({ currentUser, onSettings, onLogout, onNavigate}, ref) => { 
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  const handleOutsideClick = (event) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
      setDropdownOpen(false);
    }
  };

  useEffect(() => {
    if (dropdownOpen) {
      document.addEventListener('mousedown', handleOutsideClick);
    } else {
      document.removeEventListener('mousedown', handleOutsideClick);
    }

    return () => {
      document.removeEventListener('mousedown', handleOutsideClick);
    };
  }, [dropdownOpen]);

  return (
    <div className="user-dropdown" ref={ref}>
      <button className="dropdown-toggle" onClick={toggleDropdown}>
        {currentUser?.username || 'User'}
      </button>
      {dropdownOpen && (
        <div className="dropdown-menu" ref={dropdownRef}>

          <button onClick={onSettings}>Settings</button>
          <button onClick={onLogout}>Logout</button>
        </div>
      )}
    </div>
  );
});

export default UserDropdown;
