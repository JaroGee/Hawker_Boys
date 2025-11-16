import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth/options';
import { assertRole } from '@/lib/rbac';
import { prisma } from '@/lib/prisma';

export async function GET() {
  const session = await getServerSession(authOptions);
  assertRole(session?.user.role, 'ADMIN');
  const rows = await prisma.assessment.findMany({ include: { trainee: true, mentor: true, template: true }, orderBy: { createdAt: 'desc' } });
  const header = 'trainee,mentor,template,scores,notes,createdAt\n';
  const csv =
    header +
    rows
      .map((row) => [row.trainee?.name ?? row.traineeId, row.mentor?.email ?? row.mentorId, row.template?.name ?? row.templateId, JSON.stringify(row.scores), JSON.stringify(row.notes ?? ''), row.createdAt.toISOString()].join(','))
      .join('\n');
  return new NextResponse(csv, {
    headers: {
      'Content-Type': 'text/csv',
      'Content-Disposition': 'attachment; filename="mentor-assessments.csv"'
    }
  });
}
