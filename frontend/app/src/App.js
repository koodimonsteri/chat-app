import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import UserSettings from './pages/UserSettings';
import ChatRoom from './pages/ChatRoom';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/user/settings" element={<UserSettings />} />
        <Route path="/chat/:chatId" element={<ChatRoom/> }/>
      </Routes>
    </Router>
  );
};

export default App;