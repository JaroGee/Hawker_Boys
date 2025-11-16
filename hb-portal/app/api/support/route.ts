import { NextResponse } from 'next/server';
import { getSession } from '../../../lib/auth/session';
import { prisma } from '../../../lib/db';

export async function GET() {
  const session = await getSession();
  if (!session?.user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  const tickets = await prisma.supportTicket.findMany({
    orderBy: { createdAt: 'desc' },
    include: {
      trainee: { select: { name: true } },
      responder: { select: { name: true } }
    }
  });
  return NextResponse.json({ tickets });
}
