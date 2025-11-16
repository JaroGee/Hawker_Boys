import { prisma } from '../../../lib/db';
import { Card, CardContent, CardHeader } from '../../../components/ui/Card';
import { formatDate } from '../../../lib/utils';

export default async function MessagesPage() {
  const tickets = await prisma.supportTicket.findMany({
    include: {
      trainee: { select: { name: true } },
      responder: { select: { name: true } }
    },
    orderBy: { createdAt: 'desc' }
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-ink">Helpdesk Messages</h1>
      <div className="grid gap-4">
        {tickets.map((ticket) => (
          <Card key={ticket.id}>
            <CardHeader title={`${ticket.category} · ${ticket.trainee.name}`} description={`Status: ${ticket.status}`} />
            <CardContent>
              <p>{ticket.message}</p>
              <p className="text-xs text-ink-subtle">Opened {formatDate(ticket.createdAt)}</p>
              {ticket.responder ? (
                <p className="text-xs text-ink-subtle">Responder: {ticket.responder.name}</p>
              ) : null}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
