import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET() {
  const trainees = await prisma.traineeProfile.findMany({ include: { user: true } });
  return NextResponse.json(trainees.map((t) => ({ id: t.userId, name: t.name, email: t.user.email })));
}
