import { ReactNode } from 'react';
import { Card } from '@/components/ui/card';

interface DashboardShellProps {
  title: string;
  description?: string;
  actions?: ReactNode;
  children: ReactNode;
}

export function DashboardShell({ title, description, actions, children }: DashboardShellProps) {
  return (
    <section className="space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="font-display text-2xl font-bold text-brand-dark">{title}</h2>
          {description && <p className="text-sm text-slate-600">{description}</p>}
        </div>
        {actions}
      </header>
      <Card>{children}</Card>
    </section>
  );
}
