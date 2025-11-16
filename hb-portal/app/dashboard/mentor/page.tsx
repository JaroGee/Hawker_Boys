import { prisma } from '@/lib/prisma';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableCell, TableHeader, TableRow } from '@/components/ui/table';

export default async function MentorDashboard() {
  const [assessments, tickets] = await Promise.all([
    prisma.assessment.findMany({ include: { trainee: true, template: true }, orderBy: { createdAt: 'desc' }, take: 10 }),
    prisma.supportTicket.findMany({ where: { status: { not: 'CLOSED' } }, include: { trainee: true }, take: 5 })
  ]);

  return (
    <div className="space-y-8">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Mentor ops</h1>
      <Card>
        <CardHeader>
          <CardTitle>Recent assessments</CardTitle>
          <CardDescription>Scores and notes</CardDescription>
        </CardHeader>
        <Table>
          <TableHeader>
            <TableRow>
              <TableCell>Trainee</TableCell>
              <TableCell>Template</TableCell>
              <TableCell>Score</TableCell>
              <TableCell>Created</TableCell>
            </TableRow>
          </TableHeader>
          <tbody>
            {assessments.map((row) => (
              <TableRow key={row.id}>
                <TableCell>{row.trainee?.name ?? row.traineeId}</TableCell>
                <TableCell>{row.template?.name}</TableCell>
                <TableCell>{row.scores.map((s) => s.value).join(', ')}</TableCell>
                <TableCell>{row.createdAt.toLocaleDateString()}</TableCell>
              </TableRow>
            ))}
          </tbody>
        </Table>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Support tickets</CardTitle>
          <CardDescription>Aftercare items to resolve</CardDescription>
        </CardHeader>
        <ul className="space-y-3">
          {tickets.map((ticket) => (
            <li key={ticket.id} className="rounded border border-brand-muted p-4">
              <p className="font-medium">{ticket.category}</p>
              <p className="text-sm text-slate-600">{ticket.message}</p>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
