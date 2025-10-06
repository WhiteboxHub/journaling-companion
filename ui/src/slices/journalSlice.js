// src/redux/slices/journalSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getEntries, postEntry } from '../../utils/api';

export const fetchEntries = createAsyncThunk('journal/fetchEntries', async () => {
  return await getEntries();
});

export const submitEntry = createAsyncThunk('journal/submitEntry', async (entryText) => {
  return await postEntry(entryText);
});

const journalSlice = createSlice({
  name: 'journal',
  initialState: {
    entries: [],
    loading: false
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchEntries.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchEntries.fulfilled, (state, action) => {
        state.entries = action.payload;
        state.loading = false;
      })
      .addCase(submitEntry.fulfilled, (state, action) => {
        state.entries.unshift(action.payload);
      });
  }
});

export default journalSlice.reducer;