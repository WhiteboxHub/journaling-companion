import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchEntries } from './redux/slices/journalSlice';
import JournalDashboard from './components/JournalDashboard';
import ChatInterface from './components/ChatInterface';

function App() {
  const dispatch = useDispatch();
  const { entries, loading } = useSelector((state) => state.journal);

  useEffect(() => {
    dispatch(fetchEntries());
  }, [dispatch]);

  return (
    <div className="App max-w-4xl mx-auto p-6 space-y-10">
      <header>
        <h1 className="text-3xl font-bold text-center mb-4">📝 Journaling Companion</h1>
      </header>

      {/* Chat Interface for conversational journaling */}
      <ChatInterface />

      <hr className="my-6" />

      {/* Dashboard for viewing entries */}
      <JournalDashboard entries={entries} loading={loading} />
    </div>
  );
}

export default App;