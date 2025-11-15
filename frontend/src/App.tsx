import { Routes, Route, Navigate, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import SyncStatus from './pages/SyncStatus';

const App = () => {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1>Hawker Boys TMS</h1>
        <nav>
          <ul>
            <li><Link to="/">Dashboard</Link></li>
            <li><Link to="/sync-status">SSG Sync Status</Link></li>
          </ul>
        </nav>
      </aside>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/sync-status" element={<SyncStatus />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;
