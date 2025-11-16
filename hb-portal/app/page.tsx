import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const highlights = [
  {
    title: 'Unified training journeys',
    body: 'Track WSQ certifications, quests, compliance, and shifts in one secure workspace.'
  },
  {
    title: 'Mentor intelligence',
    body: 'Assessment templates, live location check-ins, and aftercare ticketing keep mentors looped in.'
  },
  {
    title: 'Employer-ready',
    body: 'Shift planning, attendance, and customer feedback loops give employers instant context.'
  }
];

export default function LandingPage() {
  return (
    <div className="space-y-10">
      <section className="rounded-3xl bg-gradient-to-r from-brand-primary to-brand-secondary px-8 py-12 text-white">
        <p className="text-sm uppercase tracking-[0.35em] text-white/80">Hawker Boys</p>
        <h1 className="mt-4 max-w-3xl font-display text-4xl font-bold">A care-first portal for trainees, mentors, employers, and admins.</h1>
        <p className="mt-4 max-w-2xl text-lg text-white/90">
          Built for PDPA compliance, live programme oversight, and the camaraderie of the hawker craft. Integrates with the TMS
          via secure APIs.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <Button asChild>
            <Link href="/auth/sign-in">Sign in</Link>
          </Button>
          <Button variant="secondary" asChild>
            <Link href="/public/feedback">Public feedback</Link>
          </Button>
        </div>
      </section>
      <section className="grid gap-6 md:grid-cols-3">
        {highlights.map((item) => (
          <Card key={item.title}>
            <CardHeader>
              <CardTitle>{item.title}</CardTitle>
              <CardDescription>{item.body}</CardDescription>
            </CardHeader>
          </Card>
        ))}
      </section>
    </div>
  );
}
