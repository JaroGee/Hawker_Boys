import { prisma } from '../../../lib/db';
import { Card, CardContent, CardHeader } from '../../../components/ui/Card';

export default async function ProgressPage() {
  const trainees = await prisma.traineeProfile.findMany({
    include: {
      certifications: { include: { certification: true } },
      questProgress: { include: { quest: true } },
      badges: { include: { badge: true } }
    }
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-ink">Progress & Certifications</h1>
      <div className="grid gap-6">
        {trainees.map((trainee) => (
          <Card key={trainee.userId}>
            <CardHeader title={trainee.name} description={trainee.cohort ?? 'Active trainee'} />
            <CardContent>
              <div className="grid gap-4 md:grid-cols-3">
                <div>
                  <h3 className="text-sm font-semibold text-ink">Certifications</h3>
                  <ul className="mt-2 space-y-2 text-sm text-ink-subtle">
                    {trainee.certifications.map((item) => (
                      <li key={item.id}>
                        {item.certification.name} - {item.certification.level ? `Level ${item.certification.level}` : 'Elective'}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-ink">Quests</h3>
                  <ul className="mt-2 space-y-2 text-sm text-ink-subtle">
                    {trainee.questProgress.map((progress) => (
                      <li key={progress.id}>
                        {progress.quest.title} - {progress.status}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-ink">Badges</h3>
                  <ul className="mt-2 space-y-2 text-sm text-ink-subtle">
                    {trainee.badges.map((badge) => (
                      <li key={badge.id}>{badge.badge.title}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
