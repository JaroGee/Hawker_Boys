'use client';

import { useState } from 'react';
import useSWR from 'swr';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Turnstile } from '@/components/turnstile';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function PublicFeedbackPage() {
  const { data: trainees } = useSWR('/api/trainees', fetcher);
  const [form, setForm] = useState({ traineeId: '', rating: 5, comment: '', receiptCode: '' });
  const [turnstileToken, setTurnstileToken] = useState('dev-token');
  const [message, setMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, rating: Number(form.rating), turnstileToken })
    });
    if (res.ok) {
      setMessage('Thank you for championing our trainees!');
      setForm({ traineeId: '', rating: 5, comment: '', receiptCode: '' });
    } else {
      setMessage('Submission failed. Please retry.');
    }
  };

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Public praise & feedback</h1>
      <p className="text-sm text-slate-600">Protected by Cloudflare Turnstile and rate limits to prevent spam.</p>
      <form onSubmit={handleSubmit} className="space-y-4 rounded-2xl border border-brand-muted bg-white p-6">
        <label className="block text-sm font-medium">
          Trainee
          <select
            className="mt-1 w-full rounded-md border border-brand-muted p-2"
            value={form.traineeId}
            onChange={(e) => setForm((prev) => ({ ...prev, traineeId: e.target.value }))}
          >
            <option value="">Select a trainee</option>
            {trainees?.map((trainee: any) => (
              <option key={trainee.id} value={trainee.id}>
                {trainee.name ?? trainee.email}
              </option>
            ))}
          </select>
        </label>
        <label className="block text-sm font-medium">
          Rating (1-5)
          <Input type="number" min={1} max={5} value={form.rating} onChange={(e) => setForm((prev) => ({ ...prev, rating: Number(e.target.value) }))} />
        </label>
        <label className="block text-sm font-medium">
          Comment
          <Textarea value={form.comment} onChange={(e) => setForm((prev) => ({ ...prev, comment: e.target.value }))} rows={4} />
        </label>
        <label className="block text-sm font-medium">
          Optional receipt code
          <Input value={form.receiptCode} onChange={(e) => setForm((prev) => ({ ...prev, receiptCode: e.target.value }))} />
        </label>
        <Turnstile siteKey={process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY} onVerify={(token) => setTurnstileToken(token)} />
        <Button type="submit">Share feedback</Button>
        {message && <p className="text-sm text-brand-dark">{message}</p>}
      </form>
    </div>
  );
}
