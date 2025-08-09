// src/pages/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div style={{ textAlign: 'center', marginTop: 80 }}>
      <h1>Welcome to Virtual Diary</h1>
      <p>Please choose:</p>
      <div style={{ marginTop: 20 }}>
        <Link to="/register">
          <button style={{ marginRight: 12, padding: '0.8em 1.2em' }}>Register</button>
        </Link>
        <Link to="/login">
          <button style={{ padding: '0.8em 1.2em' }}>Login</button>
        </Link>
      </div>
    </div>
  );
}
