import { NextResponse } from 'next/server';
import { getSession } from '../../../lib/auth/session';
import { prisma } from '../../../lib/db';

export async function GET() {
  const session = await getSession();
  if (!session?.user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  const traineeId = session.user.role === 'TRAINEE' ? session.user.id : undefined;
  const data = await prisma.traineeProfile.findMany({
    where: traineeId ? { userId: traineeId } : undefined,
    include: {
      certifications: { include: { certification: true } },
      questProgress: { include: { quest: true } },
      badges: { include: { badge: true } },
      compliance: true
    }
  });
  return NextResponse.json({ trainees: data });
}
