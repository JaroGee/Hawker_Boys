import { FormEvent, useState } from 'react';
import { useMutation } from '@tanstack/react-query';

import { Drawer } from '../components/Drawer';
import { FormField } from '../components/FormField';
import { useToast } from '../context/ToastContext';
import { triggerWebhookTest } from '../lib/api';

const SettingsPage = () => {
  const [secret, setSecret] = useState('');
  const toast = useToast();
  const [drawerOpen, setDrawerOpen] = useState(false);

  const mutation = useMutation({
    mutationFn: () => triggerWebhookTest(secret),
    onSuccess: () => {
      toast.push({ title: 'Webhook verified', description: 'SSG secret matched.', tone: 'success' });
      setSecret('');
    },
    onError: () => {
      toast.push({ title: 'Webhook failed', description: 'Secret mismatch.', tone: 'error' });
    },
  });

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    mutation.mutate();
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Settings</h1>
          <p className="page-subtitle">Control API, queue, and SSG integration points.</p>
        </div>
        <button type="button" className="hb-button hb-button--secondary" onClick={() => setDrawerOpen(true)}>
          View environment
        </button>
      </div>
      <div className="card">
        <h2>Webhook test</h2>
        <p className="page-subtitle">Send a smoke request to ensure Render/cron monitors accept our webhook secret.</p>
        <form onSubmit={handleSubmit}>
          <FormField label="SSG webhook secret" htmlFor="webhook-secret">
            <input
              id="webhook-secret"
              type="password"
              value={secret}
              onChange={(event) => setSecret(event.target.value)}
              required
            />
          </FormField>
          <button type="submit" className="hb-button hb-button--primary" disabled={mutation.isPending}>
            {mutation.isPending ? 'Testing…' : 'Send test call'}
          </button>
        </form>
      </div>
      <Drawer
        title="Environment"
        description="Static values baked into the UI."
        isOpen={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      >
        <p>API base URL: {import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'}</p>
        <p>Build mode: {import.meta.env.MODE}</p>
      </Drawer>
    </div>
  );
};

export default SettingsPage;
