import { prisma } from '../../../lib/db';
import { Card, CardContent, CardHeader } from '../../../components/ui/Card';
import { formatDate } from '../../../lib/utils';

export default async function SchedulePage() {
  const shifts = await prisma.shift.findMany({
    include: {
      trainee: { select: { name: true } },
      employer: { select: { companyName: true } }
    },
    orderBy: { start: 'asc' }
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-ink">Shift schedule</h1>
      <div className="grid gap-4">
        {shifts.map((shift) => (
          <Card key={shift.id}>
            <CardHeader title={`${shift.trainee.name} · ${shift.employer.companyName}`} description={shift.location} />
            <CardContent>
              <p className="text-sm text-ink">
                {formatDate(shift.start)} - {formatDate(shift.end)} ({shift.status})
              </p>
              {shift.notes ? <p className="text-sm text-ink-subtle">{shift.notes}</p> : null}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
