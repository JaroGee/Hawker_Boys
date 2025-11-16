import { Navigate, Route, Routes } from 'react-router-dom';

import { AppShell } from './components/AppShell';
import { LoadingState } from './components/LoadingState';
import { useAuth } from './context/AuthContext';
import AttendancePage from './pages/Attendance';
import ClassRunsPage from './pages/ClassRuns';
import CoursesPage from './pages/Courses';
import DashboardPage from './pages/Dashboard';
import EnrollmentsPage from './pages/Enrollments';
import LearnersPage from './pages/Learners';
import LoginPage from './pages/Login';
import SettingsPage from './pages/Settings';

const ProtectedRoute = ({ children }: { children: React.ReactElement }) => {
  const { token, initializing } = useAuth();

  if (initializing) {
    return <LoadingState label="Preparing workspace" />;
  }

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

const PublicRoute = ({ children }: { children: React.ReactElement }) => {
  const { token } = useAuth();
  if (token) {
    return <Navigate to="/dashboard" replace />;
  }
  return children;
};

const App = () => (
  <Routes>
    <Route
      path="/login"
      element={
        <PublicRoute>
          <LoginPage />
        </PublicRoute>
      }
    />
    <Route
      element={
        <ProtectedRoute>
          <AppShell />
        </ProtectedRoute>
      }
    >
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/courses" element={<CoursesPage />} />
      <Route path="/class-runs" element={<ClassRunsPage />} />
      <Route path="/learners" element={<LearnersPage />} />
      <Route path="/enrollments" element={<EnrollmentsPage />} />
      <Route path="/attendance" element={<AttendancePage />} />
      <Route path="/settings" element={<SettingsPage />} />
    </Route>
    <Route path="*" element={<Navigate to="/dashboard" replace />} />
  </Routes>
);

export default App;
