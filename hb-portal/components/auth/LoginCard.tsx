'use client';

import { FormEvent, useState } from 'react';
import { signIn } from 'next-auth/react';
import Image from 'next/image';
import { toast } from 'sonner';

export function LoginCard() {
  const [email, setEmail] = useState('');
  the [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAdminLogin = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    const result = await signIn('credentials', {
      redirect: false,
      email,
      password
    });
    setLoading(false);
    if (result?.error) {
      toast.error(result.error);
    } else {
      window.location.href = '/dashboard';
    }
  };

  const handleMagicLink = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    const result = await signIn('email', {
      redirect: false,
      email
    });
    setLoading(false);
    if (result?.error) {
      toast.error(result.error);
    } else {
      toast.success('Magic link sent. Check your email.');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-surface-muted px-4 py-16">
      <div className="w-full max-w-3xl rounded-[40px] bg-white p-10 shadow-card">
        <div className="flex flex-col items-center gap-6 text-center">
          <Image src="/favicons/portal-mark.svg" alt="Hawker Boys" width={96} height={96} />
          <h1 className="text-3xl font-bold text-ink">Welcome back to Hawker Boys Portal</h1>
          <p className="text-sm text-ink-subtle">
            Sign in with your admin credentials or request a magic link. The flame stays lit when we show up for one another.
          </p>
        </div>
        <div className="mt-10 grid gap-8 md:grid-cols-2">
          <form onSubmit={handleAdminLogin} className="space-y-4">
            <div className="text-left">
              <h2 className="text-lg font-semibold text-ink">Admin login</h2>
              <p className="text-xs text-ink-subtle">Admins authenticate with email and password.</p>
            </div>
            <label className="space-y-1 text-left text-sm font-semibold text-ink">
              Email
              <input
                type="email"
                required
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                className="mt-1 w-full rounded-2xl border border-surface-muted px-4 py-3 focus:border-brand focus:outline-none focus:ring-2 focus:ring-brand"
              />
            </label>
            <label className="space-y-1 text-left text-sm font-semibold text-ink">
              Password
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="mt-1 w-full rounded-2xl border border-surface-muted px-4 py-3 focus:border-brand focus:outline-none focus:ring-2 focus:ring-brand"
              />
            </label>
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-full bg-brand px-4 py-3 text-sm font-semibold text-white transition hover:bg-brand-dark disabled:opacity-60"
            >
              {loading ? 'Signing in...' : 'Sign in as admin'}
            </button>
          </form>
          <form onSubmit={handleMagicLink} className="space-y-4">
            <div className="text-left">
              <h2 className="text-lg font-semibold text-ink">Trainee, Mentor, Employer</h2>
              <p className="text-xs text-ink-subtle">We will email you a secure one-time link.</p>
            </div>
            <label className="space-y-1 text-left text-sm font-semibold text-ink">
              Email
              <input
                type="email"
                required
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                className="mt-1 w-full rounded-2xl border border-surface-muted px-4 py-3 focus:border-brand focus:outline-none focus:ring-2 focus:ring-brand"
              />
            </label>
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-full border border-brand px-4 py-3 text-sm font-semibold text-brand transition hover:bg-brand/10 disabled:opacity-60"
            >
              {loading ? 'Sending...' : 'Email me a magic link'}
            </button>
            <p className="text-xs text-ink-subtle">
              By signing in you agree to keep trainee data confidential and follow Hawker Boys PDPA policy.
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
