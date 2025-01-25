import React, { useState, useEffect, useRef } from 'react';
import { useUser } from '../context/UserContext';
import './UserDropdown.css';
import { fetchCurrentUser } from '../api';

const UserDropdown = React.forwardRef(({ onLogout, onNavigate }, ref) => { 
  const { currentUser, setCurrentUser } = useUser();
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

  const handleSettings = async () => {
    try {
      const userData = await fetchCurrentUser()
      setCurrentUser(userData)
    } catch(error){
      localStorage.removeItem('jwt_token');
      onNavigate('/');
    }

    onNavigate('/user/settings')
  };

  return (
    <div className="user-dropdown" ref={ref}>
      <button className="dropdown-toggle" onClick={toggleDropdown}>
        {currentUser?.username || 'User'}
      </button>
      {dropdownOpen && (
        <div className="dropdown-menu" ref={dropdownRef}>

          <button onClick={handleSettings}>Settings</button>
          <button onClick={onLogout}>Logout</button>
        </div>
      )}
    </div>
  );
});

export default UserDropdown;
