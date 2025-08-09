import React, { useEffect, useState } from 'react';
import DiaryEntryForm from '../components/DiaryEntryForm';
import EntryList from '../components/EntryList';
import { getEntries } from '../services/api';

function Dashboard({ token, username }) {
  const [entries, setEntries] = useState([]);

  // Fetch entries on mount or after a new entry is created
  const fetchEntries = async () => {
    try {
      const res = await getEntries(token);
      setEntries(res.data);
    } catch (error) {
      // Handle errors, e.g., show toast or message
      console.error("Failed to fetch entries:", error);
      setEntries([]);
    }
  };

  useEffect(() => {
    fetchEntries();
    // eslint-disable-next-line
  }, [token]);

  return (
    <main style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h2>Welcome, {username}!</h2>

      {/* Entry Creation */}
      <DiaryEntryForm token={token} onNewEntry={fetchEntries} />

      {/* Entries List */}
      <EntryList entries={entries} token={token} onChange={fetchEntries} />

      {/* Optionally add visualization, charts, stats, etc. */}
      <MoodTrendChart entries={entries} /> 
    </main>
  );
}

export default Dashboard;
