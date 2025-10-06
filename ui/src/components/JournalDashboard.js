import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { submitEntry } from '../slices/journalSlice';

function JournalDashboard({ entries, loading }) {
  const [text, setText] = useState('');
  const dispatch = useDispatch();

  const handleSubmit = () => {
    if (text.trim()) {
      dispatch(submitEntry(text));
      setText('');
    }
  };

  return (
    <div>
      <textarea
        rows="4"
        cols="50"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="How are you feeling today?"
      />
      <br />
      <button onClick={handleSubmit}>Submit Entry</button>
      <hr />
      <h2>Recent Entries</h2>
      {loading ? <p>Loading...</p> : (
        <ul>
          {entries.map((e, i) => (
            <li key={i}><strong>{e.date}</strong>: {e.entry}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default JournalDashboard;
