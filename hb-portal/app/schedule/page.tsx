import { prisma } from '@/lib/prisma';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { formatDate } from '@/lib/utils';

export default async function SchedulePage() {
  const [shifts, compliance] = await Promise.all([
    prisma.shift.findMany({ orderBy: { start: 'asc' } }),
    prisma.complianceEvent.findMany({ orderBy: { start: 'asc' } })
  ]);
  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Schedule & Compliance</h1>
      <Card>
        <CardHeader>
          <CardTitle>Shifts</CardTitle>
          <CardDescription>Employer planned</CardDescription>
        </CardHeader>
        <ul className="space-y-3">
          {shifts.map((shift) => (
            <li key={shift.id} className="rounded border border-brand-muted px-4 py-3">
              <strong>{shift.location}</strong> · {formatDate(shift.start)}
            </li>
          ))}
        </ul>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Compliance</CardTitle>
          <CardDescription>Urine tests, leave, appointments</CardDescription>
        </CardHeader>
        <ul className="space-y-3">
          {compliance.map((event) => (
            <li key={event.id} className="rounded border border-brand-muted px-4 py-3">
              <strong>{event.type}</strong> · {formatDate(event.start)}
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
