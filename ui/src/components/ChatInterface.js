// src/components/ChatInterface.js
import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';
const USER_ID = 'user_01';

function ChatInterface() {
  const [chatLog, setChatLog] = useState([]);
  const [entryText, setEntryText] = useState('');
  const [generatedPrompt, setGeneratedPrompt] = useState('');

  const generatePrompt = async () => {
    const res = await axios.post(`${API_BASE}/generate_prompt`, {
      user_id: USER_ID,
      query_text: "I've been journaling lately and want to reflect."
    });
    setGeneratedPrompt(res.data.prompt);
    setChatLog((prev) => [...prev, { role: 'bot', text: res.data.prompt }]);
  };

  const submitResponse = async () => {
    if (!entryText.trim()) return;
    const today = new Date().toISOString().split('T')[0];

    await axios.post(`${API_BASE}/submit_entry`, {
      user_id: USER_ID,
      date: today,
      entry: entryText,
      prompt: generatedPrompt
    });

    setChatLog((prev) => [...prev, { role: 'user', text: entryText }]);
    setEntryText('');
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">🗣️ Chat Interface</h2>
      <button onClick={generatePrompt} className="px-4 py-2 bg-blue-500 text-white rounded">
        Generate Prompt
      </button>
      <div className="border p-4 h-64 overflow-y-auto bg-gray-50">
        {chatLog.map((msg, i) => (
          <div key={i} className={`mb-2 ${msg.role === 'bot' ? 'text-blue-700' : 'text-gray-800'}`}>
            <strong>{msg.role === 'bot' ? 'Companion:' : 'You:'}</strong> {msg.text}
          </div>
        ))}
      </div>
      <textarea
        rows="4"
        value={entryText}
        onChange={(e) => setEntryText(e.target.value)}
        placeholder="Write your response..."
        className="w-full border p-2 rounded"
      />
      <button onClick={submitResponse} className="px-4 py-2 bg-green-500 text-white rounded">
        Submit Response
      </button>
    </div>
  );
}

export default ChatInterface;
