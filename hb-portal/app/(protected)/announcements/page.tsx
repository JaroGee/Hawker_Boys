import { prisma } from '../../../lib/db';
import { Card, CardContent, CardHeader } from '../../../components/ui/Card';
import { formatDate } from '../../../lib/utils';

export default async function AnnouncementsPage() {
  const announcements = await prisma.announcement.findMany({
    orderBy: { publishedAt: 'desc' }
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-ink">Announcements</h1>
      <div className="grid gap-4">
        {announcements.map((announcement) => (
          <Card key={announcement.id}>
            <CardHeader title={announcement.title} description={`Audience: ${announcement.audience}`} />
            <CardContent>
              <p>{announcement.body}</p>
              <p className="text-xs text-ink-subtle">Published {formatDate(announcement.publishedAt)}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
