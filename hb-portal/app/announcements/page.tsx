import { prisma } from '@/lib/prisma';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { formatDate } from '@/lib/utils';

export default async function AnnouncementsPage() {
  const announcements = await prisma.announcement.findMany({ orderBy: { publishedAt: 'desc' }, take: 20 });
  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Announcements</h1>
      {announcements.map((announcement) => (
        <Card key={announcement.id}>
          <CardHeader>
            <CardTitle>{announcement.title}</CardTitle>
            <CardDescription>{formatDate(announcement.publishedAt ?? new Date())}</CardDescription>
          </CardHeader>
          <p>{announcement.body}</p>
        </Card>
      ))}
    </div>
  );
}
