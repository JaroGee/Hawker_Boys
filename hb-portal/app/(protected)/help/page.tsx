import { prisma } from '../../../lib/db';
import { Card, CardContent, CardHeader } from '../../../components/ui/Card';

export default async function HelpPage() {
  const contacts = await prisma.emergencyContact.findMany({ include: { trainee: true } });
  const tickets = await prisma.supportTicket.findMany({ orderBy: { createdAt: 'desc' }, take: 5 });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-ink">Aftercare & Help</h1>
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader title="Emergency contacts" description="Fast reach-out list per trainee." />
          <CardContent>
            <ul className="space-y-3 text-sm text-ink">
              {contacts.map((contact) => (
                <li key={contact.id} className="rounded-2xl bg-surface-muted px-4 py-3">
                  <p className="font-semibold">{contact.name}</p>
                  <p className="text-xs text-ink-subtle">
                    {contact.relationship} · {contact.phone} · for {contact.trainee.name}
                  </p>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
        <Card>
          <CardHeader title="Recent support tickets" description="Monitor outstanding cases." />
          <CardContent>
            <ul className="space-y-3 text-sm text-ink">
              {tickets.map((ticket) => (
                <li key={ticket.id} className="rounded-2xl bg-surface-muted px-4 py-3">
                  <p className="font-semibold">{ticket.category}</p>
                  <p className="text-xs text-ink-subtle">Status: {ticket.status}</p>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
