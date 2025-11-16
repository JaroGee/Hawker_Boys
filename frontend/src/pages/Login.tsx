import { FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import flameMark from '../assets/logo-flame.png';
import wordmark from '../assets/logo-wordmark.png';

const DEFAULT_CREDENTIALS = {
  email: 'admin@hawkerboys.local',
  password: 'ChangeMe123!',
};

const LoginPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const toast = useToast();
  const [form, setForm] = useState(DEFAULT_CREDENTIALS);
  const [remember, setRemember] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setSubmitting(true);
    try {
      await login({ ...form, remember });
      navigate('/dashboard');
    } catch (error) {
      toast.push({
        title: 'Unable to sign in',
        description: 'Please verify your credentials and try again.',
        tone: 'error',
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="content-area" style={{ maxWidth: 420, margin: '0 auto' }}>
      <div className="card">
        <div className="sidebar__logo" style={{ marginBottom: 'var(--hb-space-lg)' }}>
          <img src={flameMark} alt="Hawker Boys flame" width={48} height={48} />
          <img src={wordmark} alt="Hawker Boys wordmark" height={32} />
        </div>
        <h1 className="page-title">Welcome back</h1>
        <p className="page-subtitle">Sign in to manage learners, runs, and SSG syncs.</p>
        <form onSubmit={handleSubmit}>
          <div className="form-field">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              required
              value={form.email}
              onChange={(event) => setForm((prev) => ({ ...prev, email: event.target.value }))}
            />
          </div>
          <div className="form-field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              required
              value={form.password}
              onChange={(event) => setForm((prev) => ({ ...prev, password: event.target.value }))}
            />
          </div>
          <label style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}>
            <input type="checkbox" checked={remember} onChange={(event) => setRemember(event.target.checked)} />
            Remember me on this device
          </label>
          <button type="submit" className="hb-button hb-button--primary" disabled={submitting}>
            {submitting ? 'Signing in…' : 'Sign in'}
          </button>
        </form>
        <p className="page-subtitle">Use the default credentials above for first-time access.</p>
      </div>
    </div>
  );
};

export default LoginPage;
