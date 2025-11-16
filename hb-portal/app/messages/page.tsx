import { prisma } from '@/lib/prisma';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default async function MessagesPage() {
  const tickets = await prisma.supportTicket.findMany({ orderBy: { createdAt: 'desc' }, take: 15, include: { trainee: true } });
  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Messages & Aftercare</h1>
      <Card>
        <CardHeader>
          <CardTitle>Tickets</CardTitle>
          <CardDescription>Secure help desk threads</CardDescription>
        </CardHeader>
        <ul className="space-y-4">
          {tickets.map((ticket) => (
            <li key={ticket.id} className="rounded border border-brand-muted p-4">
              <p className="font-semibold">{ticket.category}</p>
              <p className="text-sm text-slate-600">{ticket.message}</p>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
