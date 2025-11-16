import { prisma } from '../../../lib/db';
import { Card, CardContent, CardHeader } from '../../../components/ui/Card';
import { formatDate } from '../../../lib/utils';

export default async function UploadsPage() {
  const documents = await prisma.secureDocument.findMany({
    orderBy: { createdAt: 'desc' },
    include: { owner: { select: { email: true, role: true } } }
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-ink">Secure uploads</h1>
      <Card>
        <CardHeader title="Recent documents" description="Only show metadata to keep files private." />
        <CardContent>
          <table className="w-full table-fixed text-left text-sm">
            <thead className="text-xs uppercase tracking-wide text-ink-subtle">
              <tr>
                <th className="py-2">Owner</th>
                <th>Category</th>
                <th>Filename</th>
                <th>Size</th>
                <th>Uploaded</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-muted">
              {documents.map((doc) => (
                <tr key={doc.id} className="text-ink">
                  <td className="py-3">{doc.ownerType} · {doc.owner.email}</td>
                  <td>{doc.category}</td>
                  <td>{doc.filename}</td>
                  <td>{(doc.size / 1024).toFixed(1)} KB</td>
                  <td>{formatDate(doc.createdAt)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}
