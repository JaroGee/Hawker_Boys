import { prisma } from '@/lib/prisma';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';

export default async function ProgressPage() {
  const [certifications, quests] = await Promise.all([
    prisma.traineeCertification.findMany({ include: { certification: true } }),
    prisma.questProgress.findMany({ include: { quest: true } })
  ]);
  const completion = (certifications.length / Math.max(1, quests.length)) * 100;
  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Progress & Achievements</h1>
      <Card>
        <CardHeader>
          <CardTitle>WSQ milestones</CardTitle>
          <CardDescription>Food Safety and internal modules</CardDescription>
        </CardHeader>
        <Progress value={completion} />
        <div className="mt-4 flex flex-wrap gap-3">
          {certifications.map((item) => (
            <Badge key={item.certificationId} label={item.certification?.name ?? 'Certification'} />
          ))}
        </div>
      </Card>
    </div>
  );
}
