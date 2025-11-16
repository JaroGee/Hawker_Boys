import { prisma } from '@/lib/prisma';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default async function BadgesPage() {
  const badges = await prisma.badge.findMany({ orderBy: { title: 'asc' } });
  const earned = await prisma.traineeBadge.findMany({ include: { badge: true } });
  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Badges & Ranks</h1>
      <section className="grid gap-4 md:grid-cols-3">
        {badges.map((badge) => (
          <Card key={badge.id}>
            <CardHeader>
              <CardTitle>{badge.title}</CardTitle>
              <CardDescription>{badge.description}</CardDescription>
            </CardHeader>
            <p className="text-sm text-slate-500">Code: {badge.code}</p>
          </Card>
        ))}
      </section>
      <Card>
        <CardHeader>
          <CardTitle>Earned highlights</CardTitle>
        </CardHeader>
        <ul className="space-y-2">
          {earned.map((item) => (
            <li key={item.id} className="text-sm">
              {item.badge?.title} · {item.awardedAt.toLocaleDateString()}
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
