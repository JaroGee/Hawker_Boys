import { prisma } from '@/lib/prisma';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export default async function QuestsPage() {
  const quests = await prisma.quest.findMany({ orderBy: { startAt: 'asc' } });
  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Quests</h1>
      <div className="grid gap-4 md:grid-cols-2">
        {quests.map((quest) => (
          <Card key={quest.id}>
            <CardHeader>
              <CardTitle>{quest.title}</CardTitle>
              <CardDescription>{quest.description}</CardDescription>
            </CardHeader>
            <div className="flex items-center justify-between text-xs text-slate-500">
              <Badge label={`${quest.points} pts`} />
              <p>
                {quest.startAt ? new Date(quest.startAt).toLocaleDateString() : 'Now'} —
                {quest.endAt ? new Date(quest.endAt).toLocaleDateString() : 'Open'}
              </p>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
