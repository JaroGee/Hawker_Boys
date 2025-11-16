import { prisma } from '@/lib/prisma';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default async function EmployerDashboard() {
  const [shifts, feedback] = await Promise.all([
    prisma.shift.findMany({ orderBy: { start: 'asc' }, take: 6 }),
    prisma.customerFeedback.findMany({ include: { trainee: true }, orderBy: { createdAt: 'desc' }, take: 5 })
  ]);

  return (
    <div className="space-y-8">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Employer hub</h1>
      <Card>
        <CardHeader>
          <CardTitle>Shift planner</CardTitle>
          <CardDescription>Confirm and share rosters</CardDescription>
        </CardHeader>
        <div className="grid gap-3 md:grid-cols-2">
          {shifts.map((shift) => (
            <div key={shift.id} className="rounded border border-brand-muted p-4">
              <p className="font-medium">{shift.location}</p>
              <p className="text-sm text-slate-600">{new Date(shift.start).toLocaleString()}</p>
            </div>
          ))}
        </div>
        <Button className="mt-4" variant="secondary">
          Export trainee iCal
        </Button>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Customer feedback pulse</CardTitle>
          <CardDescription>Celebrate wins and resolve concerns</CardDescription>
        </CardHeader>
        <ul className="space-y-3">
          {feedback.map((item) => (
            <li key={item.id} className="rounded border border-brand-muted p-4">
              <p className="font-semibold">{item.trainee?.name ?? item.traineeId}</p>
              <p className="text-sm">Rating {item.rating} · {item.comment}</p>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
