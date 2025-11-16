'use client';

import { signIn } from 'next-auth/react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';

export default function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [supportNote, setSupportNote] = useState('');
  const [supportResponse, setSupportResponse] = useState<string | null>(null);

  const handleAdminSignIn = async () => {
    setLoading(true);
    setMessage(null);
    const result = await signIn('credentials', { redirect: false, email, password });
    if (result?.error) {
      setMessage('Invalid credentials');
    } else {
      setMessage('Redirecting...');
    }
    setLoading(false);
  };

  const handleMagicLink = async () => {
    setLoading(true);
    setMessage('Check your inbox for the secure link.');
    await signIn('email', { email, redirect: false });
    setLoading(false);
  };

  const handleSupport = async () => {
    setSupportResponse(null);
    await fetch('/api/support', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: supportNote, category: 'LOGIN' })
    });
    setSupportResponse('Thanks! The ops team will reach out.');
    setSupportNote('');
  };

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Welcome back</CardTitle>
          <CardDescription>Admins sign in with credentials. Trainees, mentors, and employers use magic links.</CardDescription>
        </CardHeader>
        <div className="space-y-4">
          <Input value={email} onChange={(e) => setEmail(e.target.value)} type="email" placeholder="Email" />
          <Input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="Admin password" />
          <div className="flex flex-wrap gap-3">
            <Button onClick={handleAdminSignIn} disabled={loading}>
              Admin sign in
            </Button>
            <Button variant="secondary" onClick={handleMagicLink} disabled={loading}>
              Email me a magic link
            </Button>
          </div>
          {message && <p className="text-sm text-brand-dark">{message}</p>}
        </div>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Need help?</CardTitle>
          <CardDescription>Reach the Hawker Boys ops team securely.</CardDescription>
        </CardHeader>
        <Textarea placeholder="Let us know how we can help." rows={4} value={supportNote} onChange={(e) => setSupportNote(e.target.value)} />
        <Button className="mt-4" variant="outline" type="button" onClick={handleSupport} disabled={!supportNote}>
          Submit support note
        </Button>
        {supportResponse && <p className="text-sm text-brand-dark">{supportResponse}</p>}
      </Card>
    </div>
  );
}
