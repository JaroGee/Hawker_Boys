'use client';

import useSWR from 'swr';
import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function AdminAnnouncementsPage() {
  const { data, mutate } = useSWR('/api/announcements', fetcher);
  const [form, setForm] = useState({ title: '', body: '', audience: 'ALL' });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('/api/announcements', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    setForm({ title: '', body: '', audience: 'ALL' });
    mutate();
  };

  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Announcements admin</h1>
      <form onSubmit={handleSubmit} className="space-y-4 rounded-2xl border border-brand-muted bg-white p-6">
        <Input value={form.title} onChange={(e) => setForm((prev) => ({ ...prev, title: e.target.value }))} placeholder="Title" />
        <Textarea value={form.body} onChange={(e) => setForm((prev) => ({ ...prev, body: e.target.value }))} rows={5} placeholder="Body" />
        <label className="block text-sm font-medium">
          Audience
          <select className="mt-1 w-full rounded-md border border-brand-muted p-2" value={form.audience} onChange={(e) => setForm((prev) => ({ ...prev, audience: e.target.value }))}>
            <option value="ALL">All</option>
            <option value="TRAINEES">Trainees</option>
            <option value="MENTORS">Mentors</option>
            <option value="EMPLOYERS">Employers</option>
          </select>
        </label>
        <Button type="submit">Publish</Button>
      </form>
      <section className="space-y-3">
        {data?.map((item: any) => (
          <div key={item.id} className="rounded border border-brand-muted p-4">
            <p className="text-xs uppercase text-slate-500">{item.audience}</p>
            <h2 className="font-semibold">{item.title}</h2>
            <p className="text-sm text-slate-600">{item.body}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
