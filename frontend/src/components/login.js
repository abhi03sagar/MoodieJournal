// src/components/AuthForm.js
import React, { useState } from 'react';

function AuthorizationForm({ onAuthorization }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); // error state 
  const [loading, setLoading] = useState(false);

  const handleSubmission = async (e) => {
    e.preventDefault(); // stop default form reload
    setError(null);     // clear any previous errors
    setLoading(true);
    try {
      const response = await fetch(process.env.REACT_APP_API_URL + '/api/auth/login', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json',
          'Accept': 'application/json',
         },
        body: JSON.stringify({ username, password }),
      });

      // Checks HTTP status
      if (!response.ok) {
        let msg;
        switch(response.status){
          case 400:
            msg="Please fill in all required fields.";
          case 401:
            msg="Wrong username or password.";
          case 429:
            msg="Too many attempts. Please wait before trying again.";
          default:
            msg="Server error. Please try again later.";
        }
        throw new Error(msg);
      }

      const data = await response.json();

      // Checks if token exists in response 
      if (data.accessToken) {
        onAuthorization(data.accessToken, data.username);
      } else {
        throw new Error('Unexpected response');
      }
    } catch (err) {
      console.error('Login failed:', err);
      setError(err.message);
    }
    finally{
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmission} style={{maxWidth: 300, margin: 'auto'}}>
      <input
        value={username}
        onChange={e => setUsername(e.target.value)}
        placeholder="Username"
        required
        disabled={loading}
      />
      <input
        value={password}
        onChange={e => setPassword(e.target.value)}
        type="password"
        placeholder="Password"
        required
        disabled={loading}
      />
      <button type="submit" disabled={loading} style={{width: '100%'}}>
        {loading?'Logging in...': 'Login'}</button>

      {error && <p style={{ color: 'red', marginTop: 8 }}>{error}</p>}
    </form>
  );
}

export default AuthorizationForm;