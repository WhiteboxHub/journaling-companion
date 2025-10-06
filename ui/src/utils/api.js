// src/utils/api.js
import axios from 'axios';

const API_BASE = 'http://localhost:8000';
const USER_ID = 'user_01';

export async function getEntries() {
  const res = await axios.get(`${API_BASE}/get_entries`, {
    params: { user_id: USER_ID, days: 7 }
  });
  return res.data;
}

export async function postEntry(entryText) {
  const today = new Date().toISOString().split('T')[0];
  const res = await axios.post(`${API_BASE}/submit_entry`, {
    user_id: USER_ID,
    date: today,
    entry: entryText,
    prompt: 'How are you feeling today?'
  });
  return { entry: entryText, date: today };
}