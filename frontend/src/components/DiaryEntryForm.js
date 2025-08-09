// src/components/DiaryEntryForm.js 
import React, { useState } from 'react';
import { createEntry } from '../services/api'; // Make sure this function exists in api.js

function DiaryEntryForm({ token, onNewEntry }) {
  const [entryText, setEntryText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    if (!entryText.trim()) {
      setError('Diary entry cannot be empty.');
      setLoading(false);
      return;
    }

    try {
      await createEntry(token, entryText); // API call to create the new entry
      setEntryText(''); // Clear the input after successful submission
      if (onNewEntry) {
        onNewEntry(); // Callback to tell parent (Dashboard) to refresh entry list
      }
    } catch (err) {
      console.error('Error creating entry:', err);
      setError(err.response?.data?.message || 'Failed to create diary entry.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginBottom: '2em', border: '1px solid #eee', padding: '1.5em', borderRadius: '8px' }}>
      <h3>Create New Diary Entry</h3>
      <form onSubmit={handleSubmit}>
        <textarea
          placeholder="What's on your mind today?"
          value={entryText}
          onChange={(e) => setEntryText(e.target.value)}
          rows="6"
          style={{ width: '100%', padding: '0.8em', border: '1px solid #ccc', borderRadius: '4px', resize: 'vertical' }}
          disabled={loading}
        ></textarea>
        <button
          type="submit"
          disabled={loading}
          style={{
            marginTop: '1em', padding: '0.8em 1.5em', backgroundColor: '#007bff', color: 'white',
            border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '1em'
          }}
        >
          {loading ? 'Saving Entry...' : 'Save Entry'}
        </button>
        {error && <p style={{ color: 'red', marginTop: '1em' }}>{error}</p>}
      </form>
    </div>
  );
}

export default DiaryEntryForm;