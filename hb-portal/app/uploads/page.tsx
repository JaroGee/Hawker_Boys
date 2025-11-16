import { prisma } from '@/lib/prisma';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default async function UploadsPage() {
  const documents = await prisma.secureDocument.findMany({ orderBy: { createdAt: 'desc' }, take: 10 });
  return (
    <div className="space-y-6">
      <h1 className="font-display text-3xl font-semibold text-brand-dark">Secure uploads</h1>
      <Card>
        <CardHeader>
          <CardTitle>Documents</CardTitle>
          <CardDescription>Medical leave, bank, and official correspondence</CardDescription>
        </CardHeader>
        <ul className="space-y-4">
          {documents.map((doc) => (
            <li key={doc.id} className="rounded border border-brand-muted px-4 py-3">
              <p className="font-medium">{doc.category}</p>
              <p className="text-sm text-slate-600">{doc.filename}</p>
              <p className="text-xs text-slate-500">Owner: {doc.ownerType}</p>
            </li>
          ))}
        </ul>
        <Button className="mt-4">Upload new document</Button>
      </Card>
    </div>
  );
}
