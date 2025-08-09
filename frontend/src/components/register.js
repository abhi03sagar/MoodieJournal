// frontend/src/components/Register.js
import React, { useState } from 'react';
import { register } from '../services/api';

function Register({ onRegister }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

const handleSubmit = async (e) => {
  e.preventDefault();
  setError('');
  try {
    const res = await register(username, password);
    const { accessToken, username: returnedUsername } = res.data;

    // 👇 Auto-login after registration
    onRegister(accessToken, returnedUsername);
  } catch (err) {
    setError(err.response?.data?.message || 'Error registering');
  }
};

  return (
    <form onSubmit={handleSubmit}>
      <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button type="submit">Register</button>
      {error && <p>{error}</p>}
    </form>
  );
}

export default Register;
