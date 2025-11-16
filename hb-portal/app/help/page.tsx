import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

const helplines = [
  { name: 'Ops hotline', phone: '+65 6000 1234', hours: '24/7 urgent matters' },
  { name: 'Aftercare WhatsApp', phone: '+65 8111 9999', hours: '9am-9pm daily' }
];

export default function HelpPage() {
  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Help & Aftercare</h1>
      <Card>
        <CardHeader>
          <CardTitle>Helplines</CardTitle>
          <CardDescription>Always reach a human</CardDescription>
        </CardHeader>
        <ul className="space-y-3">
          {helplines.map((item) => (
            <li key={item.name} className="rounded border border-brand-muted px-4 py-3">
              <p className="font-semibold">{item.name}</p>
              <p className="text-sm text-slate-600">{item.phone} · {item.hours}</p>
            </li>
          ))}
        </ul>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Secure message</CardTitle>
          <CardDescription>Only admins can see these submissions.</CardDescription>
        </CardHeader>
        <Textarea rows={4} placeholder="Share how we can help." />
        <Button className="mt-4">Send message</Button>
      </Card>
    </div>
  );
}
