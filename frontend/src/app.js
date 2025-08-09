import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import axiosInstance from './services/axiosInstance';

import Home from './pages/home';
import AuthorizationForm from './components/login';
import Register from './components/register';
import Dashboard from './pages/dashboard';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [username, setUsername] = useState(localStorage.getItem('username'));

  const handleAuthSuccess = (newToken, newUsername) => {
    setToken(newToken);
    setUsername(newUsername);
    localStorage.setItem('token', newToken);
    localStorage.setItem('username', newUsername);
  };

  const handleLogout = async () => {
    try {
      await axiosInstance.post('/auth/logout');
    } catch (err) {
      console.error('Logout failed:', err);
    }
    setToken(null);
    setUsername(null);
    localStorage.removeItem('token');
    localStorage.removeItem('username');
  };

  return (
    <Router>
      {token && (
        <nav style={{ padding: '1em', backgroundColor: '#f0f0f0', textAlign: 'right', borderBottom: '1px solid #ddd' }}>
          <span style={{ marginRight: '1em', fontWeight: 'bold' }}>Welcome, {username}!</span>
          <button
            onClick={handleLogout}
            style={{
              padding: '0.6em 1.2em',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              fontSize: '0.9em'
            }}
          >
            Logout
          </button>
        </nav>
      )}

      <Routes>
        <Route path="/" element={<Home />} />

        <Route
          path="/register"
          element={
            token ? <Navigate to="/dashboard" replace /> : <Register onRegister={handleAuthSuccess} />
          }
        />

        <Route
          path="/login"
          element={
            token ? <Navigate to="/dashboard" replace /> : <AuthorizationForm onAuthorization={handleAuthSuccess} />
          }
        />

        <Route
          path="/dashboard"
          element={
            token ? <Dashboard /> : <Navigate to="/" replace />
          }
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

