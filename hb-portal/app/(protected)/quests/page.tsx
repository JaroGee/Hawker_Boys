import { prisma } from '../../../lib/db';
import { Card, CardContent, CardHeader } from '../../../components/ui/Card';

export default async function QuestsPage() {
  const quests = await prisma.quest.findMany({ include: { progress: true } });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-ink">Quests</h1>
      <div className="grid gap-4">
        {quests.map((quest) => (
          <Card key={quest.id}>
            <CardHeader title={quest.title} description={`${quest.points} points`} />
            <CardContent>
              <p>{quest.description}</p>
              <p className="text-xs text-ink-subtle">
                Active trainees: {quest.progress.filter((p) => p.status === 'ACTIVE').length} / {quest.progress.length}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
