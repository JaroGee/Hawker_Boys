import { prisma } from '../../../lib/db';
import { Card, CardContent, CardHeader } from '../../../components/ui/Card';

export default async function BadgesPage() {
  const badges = await prisma.badge.findMany({ include: { awards: true } });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-ink">Badges</h1>
      <div className="grid gap-4 md:grid-cols-2">
        {badges.map((badge) => (
          <Card key={badge.id}>
            <CardHeader title={badge.title} description={badge.description} />
            <CardContent>
              <p className="text-sm font-semibold text-brand">{badge.code}</p>
              <p className="text-xs text-ink-subtle">Awarded {badge.awards.length} times</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
