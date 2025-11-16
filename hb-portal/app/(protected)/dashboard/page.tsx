import { prisma } from '../../../lib/db';
import { Card, CardContent, CardHeader } from '../../../components/ui/Card';
import { Table, TableHeader, TableRow } from '../../../components/ui/Table';
import { formatDate } from '../../../lib/utils';

export default async function DashboardPage() {
  const [announcements, traineeCount, mentors, employers, feedback] = await Promise.all([
    prisma.announcement.findMany({ orderBy: { publishedAt: 'desc' }, take: 3 }),
    prisma.traineeProfile.count(),
    prisma.mentorProfile.count(),
    prisma.employerProfile.count(),
    prisma.customerFeedback.findMany({
      orderBy: { createdAt: 'desc' },
      take: 5,
      include: { trainee: { select: { name: true } } }
    })
  ]);

  return (
    <div className="space-y-8">
      <div className="grid gap-6 md:grid-cols-4">
        <Card>
          <CardHeader title="Trainees" />
          <CardContent>
            <p className="text-3xl font-bold text-brand">{traineeCount}</p>
            <p className="text-xs uppercase text-ink-subtle">Active learners</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader title="Mentors" />
          <CardContent>
            <p className="text-3xl font-bold text-brand">{mentors}</p>
            <p className="text-xs uppercase text-ink-subtle">Guiding the flame</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader title="Employers" />
          <CardContent>
            <p className="text-3xl font-bold text-brand">{employers}</p>
            <p className="text-xs uppercase text-ink-subtle">Hiring partners</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader title="Feedback" />
          <CardContent>
            <p className="text-3xl font-bold text-brand">{feedback.length}</p>
            <p className="text-xs uppercase text-ink-subtle">Recent praises</p>
          </CardContent>
        </Card>
      </div>
      <Card>
        <CardHeader title="Latest announcements" description="Stay synced with operations." />
        <CardContent>
          <ul className="space-y-4">
            {announcements.map((item) => (
              <li key={item.id} className="rounded-2xl bg-surface-muted px-4 py-3">
                <p className="font-semibold text-ink">{item.title}</p>
                <p className="text-sm text-ink-subtle">{item.body}</p>
                <p className="text-xs text-ink-subtle">Published {formatDate(item.publishedAt)}</p>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-ink">Latest community feedback</h2>
        <Table>
          <TableHeader>
            <span>Trainee</span>
            <span>Rating</span>
            <span>Comment</span>
            <span>Receipt</span>
            <span>At</span>
          </TableHeader>
          {feedback.map((item) => (
            <TableRow key={item.id}>
              <span>{item.trainee.name}</span>
              <span>{item.rating}/5</span>
              <span className="truncate">{item.comment}</span>
              <span>{item.receiptCode ?? '—'}</span>
              <span>{formatDate(item.createdAt)}</span>
            </TableRow>
          ))}
        </Table>
      </div>
    </div>
  );
}
