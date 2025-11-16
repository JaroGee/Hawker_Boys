import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth/options';
import { assertRole } from '@/lib/rbac';
import { prisma } from '@/lib/prisma';

export async function GET() {
  const session = await getServerSession(authOptions);
  assertRole(session?.user.role, 'ADMIN');
  const rows = await prisma.customerFeedback.findMany({ include: { trainee: true }, orderBy: { createdAt: 'desc' } });
  const header = 'traineeName,rating,comment,receiptCode,createdAt\n';
  const csv =
    header +
    rows
      .map((row) => [row.trainee?.name ?? row.traineeId, row.rating, JSON.stringify(row.comment), row.receiptCode ?? '', row.createdAt.toISOString()].join(','))
      .join('\n');
  return new NextResponse(csv, {
    headers: {
      'Content-Type': 'text/csv',
      'Content-Disposition': 'attachment; filename="customer-feedback.csv"'
    }
  });
}
