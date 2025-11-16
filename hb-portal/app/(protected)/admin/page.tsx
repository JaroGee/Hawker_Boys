import { redirect } from 'next/navigation';
import { getSession } from '../../../lib/auth/session';
import { prisma } from '../../../lib/db';
import { Card, CardContent, CardHeader } from '../../../components/ui/Card';

export default async function AdminPage() {
  const session = await getSession();
  if (session?.user?.role !== 'ADMIN') {
    redirect('/dashboard');
  }
  const [assessments, auditEvents] = await Promise.all([
    prisma.assessment.findMany({
      include: {
        trainee: { select: { name: true } },
        mentor: { select: { name: true } },
        template: { select: { name: true } }
      },
      orderBy: { createdAt: 'desc' },
      take: 5
    }),
    prisma.auditEvent.findMany({ orderBy: { at: 'desc' }, take: 10 })
  ]);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-ink">Admin control room</h1>
      <Card>
        <CardHeader title="Recent assessments" />
        <CardContent>
          <ul className="space-y-3 text-sm text-ink">
            {assessments.map((assessment) => (
              <li key={assessment.id} className="rounded-2xl bg-surface-muted px-4 py-3">
                <p className="font-semibold">{assessment.template.name}</p>
                <p className="text-xs text-ink-subtle">
                  {assessment.trainee.name} · {assessment.mentor.name}
                </p>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
      <Card>
        <CardHeader title="Audit trail" description="Last 10 sensitive actions." />
        <CardContent>
          <ul className="space-y-3 text-xs uppercase tracking-wide text-ink-subtle">
            {auditEvents.map((event) => (
              <li key={event.id} className="rounded-2xl bg-surface-muted px-4 py-3">
                {event.actorRole} · {event.action} · {event.entity}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
