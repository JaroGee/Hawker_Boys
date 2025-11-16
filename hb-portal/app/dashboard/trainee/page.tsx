import { prisma } from '@/lib/prisma';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { formatDate } from '@/lib/utils';

export default async function TraineeDashboard() {
  const [announcements, certifications, quests, shifts] = await Promise.all([
    prisma.announcement.findMany({ where: { OR: [{ audience: 'ALL' }, { audience: 'TRAINEES' }] }, orderBy: { publishedAt: 'desc' }, take: 5 }),
    prisma.traineeCertification.findMany({ include: { certification: true }, take: 5 }),
    prisma.questProgress.findMany({ include: { quest: true }, where: { status: { not: 'LOCKED' } }, take: 5 }),
    prisma.shift.findMany({ orderBy: { start: 'asc' }, take: 5 })
  ]);

  const completion = (certifications.length / Math.max(1, quests.length)) * 100;

  return (
    <div className="space-y-8">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Trainee dashboard</h1>
      <Card>
        <CardHeader>
          <CardTitle>Progress</CardTitle>
          <CardDescription>WSQ achievements and quests</CardDescription>
        </CardHeader>
        <div className="space-y-4">
          <Progress value={completion} />
          <div className="flex flex-wrap gap-3">
            {certifications.map((item) => (
              <Badge key={item.certificationId} label={item.certification?.name ?? 'Certification'} />
            ))}
          </div>
        </div>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Upcoming shifts</CardTitle>
          <CardDescription>Employer confirmed sessions</CardDescription>
        </CardHeader>
        <ul className="space-y-3">
          {shifts.map((shift) => (
            <li key={shift.id} className="rounded border border-brand-muted bg-white/70 px-4 py-3">
              <p className="font-medium">{shift.location}</p>
              <p className="text-sm text-slate-600">
                {formatDate(shift.start)} · {new Date(shift.start).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </li>
          ))}
        </ul>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Announcements</CardTitle>
          <CardDescription>What is new</CardDescription>
        </CardHeader>
        <ul className="space-y-3">
          {announcements.map((item) => (
            <li key={item.id}>
              <p className="font-semibold text-brand-primary">{item.title}</p>
              <p className="text-sm text-slate-600">{item.body}</p>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
