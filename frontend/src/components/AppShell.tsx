import { useState } from 'react';
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';

import flameMark from '../assets/logo-flame.png';
import wordmark from '../assets/logo-wordmark.png';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../theme';

const navItems = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Courses', path: '/courses' },
  { label: 'Class Runs', path: '/class-runs' },
  { label: 'Learners', path: '/learners' },
  { label: 'Enrollments', path: '/enrollments' },
  { label: 'Attendance', path: '/attendance' },
  { label: 'Settings', path: '/settings' },
];

const ThemeToggle = () => {
  const { mode, toggleMode } = useTheme();
  return (
    <button type="button" className="hb-button hb-button--secondary" onClick={toggleMode}>
      {mode === 'light' ? 'Dark mode' : 'Light mode'}
    </button>
  );
};

const UserSummary = () => {
  const { profile, logout } = useAuth();
  const initials = profile?.full_name
    ?.split(' ')
    .map((name) => name[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();
  return (
    <div className="header-actions">
      <div className="chip" aria-label={`Signed in as ${profile?.full_name ?? 'Operator'}`}>
        {initials || 'HB'}
      </div>
      <button type="button" className="hb-button hb-button--ghost" onClick={logout}>
        Logout
      </button>
    </div>
  );
};

export const AppShell = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="app-shell">
      <aside className="sidebar" data-open={sidebarOpen}>
        <div>
          <button
            type="button"
            className="hb-button hb-button--ghost"
            onClick={() => navigate('/dashboard')}
            aria-label="Go to dashboard"
          >
            <div className="sidebar__logo">
              <img src={flameMark} alt="Hawker Boys flame" width={32} height={32} />
              <img src={wordmark} alt="Hawker Boys wordmark" height={26} />
            </div>
          </button>
          <nav aria-label="Main navigation">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) => `${isActive ? 'active' : ''}`}
                onClick={() => setSidebarOpen(false)}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
        <p className="page-subtitle">Build brighter learning journeys.</p>
      </aside>
      <div className="main-shell">
        <header className="app-header">
          <div className="input-group">
            <button
              type="button"
              className="hb-button hb-button--secondary"
              onClick={() => setSidebarOpen((prev) => !prev)}
            >
              Menu
            </button>
            <div>
              <h1 className="page-title">
                {navItems.find((item) => location.pathname.startsWith(item.path))?.label ?? 'Dashboard'}
              </h1>
              <p className="page-subtitle">Hawker Boys Training Management</p>
            </div>
          </div>
          <div className="header-actions">
            <ThemeToggle />
            <UserSummary />
          </div>
        </header>
        <main className="content-area">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
