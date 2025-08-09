// frontend/src/components/EntryList.js
import React from 'react';
import { deleteEntry, editEntry, downloadPDF } from '../services/api';

function EntryList({ entries, token, onChange }) {
  const handleDelete = async (id) => {
    await deleteEntry(token, id);
    if (onChange) onChange();
  };

  const handleDownload = async (id) => {
    const res = await downloadPDF(token, id);
    const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'diary_entry.pdf');
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
  };

  return (
    <div>
      <h3>Your Diary Entries:</h3>
      {entries.length === 0 ? (
        <p>No entries yet.</p>
      ) : (
        entries.map(entry => (
          <div key={entry._id} style={{ border: '1px solid #ccc', margin: '1em 0', padding: '1em' }}>
            <div>{entry.text}</div>
            <div><strong>Sentiment: {entry.sentiment}</strong></div>
            <button onClick={() => handleDelete(entry._id)}>Delete</button>
            <button onClick={() => handleDownload(entry._id)}>Download PDF</button>
          </div>
        ))
      )}
    </div>
  );
}

export default EntryList;
