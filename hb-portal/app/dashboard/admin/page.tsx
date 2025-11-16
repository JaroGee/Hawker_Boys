import Link from 'next/link';
import { prisma } from '@/lib/prisma';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default async function AdminDashboard() {
  const [counts, announcements, audits] = await Promise.all([
    prisma.user.groupBy({ by: ['role'], _count: true }),
    prisma.announcement.findMany({ take: 3, orderBy: { publishedAt: 'desc' } }),
    prisma.auditEvent.findMany({ take: 5, orderBy: { at: 'desc' } })
  ]);
  return (
    <div className="space-y-8">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Admin control center</h1>
      <Card>
        <CardHeader>
          <CardTitle>People snapshot</CardTitle>
          <CardDescription>System user counts</CardDescription>
        </CardHeader>
        <dl className="grid gap-4 md:grid-cols-4">
          {counts.map((row) => (
            <div key={row.role} className="rounded border border-brand-muted p-4">
              <dt className="text-xs uppercase text-slate-500">{row.role}</dt>
              <dd className="text-3xl font-bold">{row._count}</dd>
            </div>
          ))}
        </dl>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Announcements</CardTitle>
          <CardDescription>Manage platform updates</CardDescription>
        </CardHeader>
        <div className="space-y-4">
          {announcements.map((item) => (
            <div key={item.id} className="rounded border border-brand-muted p-4">
              <p className="font-semibold">{item.title}</p>
              <p className="text-sm text-slate-600">{item.body}</p>
            </div>
          ))}
          <Button asChild>
            <Link href="/admin/announcements">Create announcement</Link>
          </Button>
        </div>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Audit log</CardTitle>
          <CardDescription>Last five events</CardDescription>
        </CardHeader>
        <ul className="space-y-2 text-sm">
          {audits.map((event) => (
            <li key={event.id} className="rounded border border-brand-muted px-4 py-2">
              <strong>{event.actorRole}</strong> {event.action} {event.entity} · {new Date(event.at).toLocaleString()}
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
