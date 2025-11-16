import { NextResponse } from 'next/server';
import { prisma } from '../../../lib/db';

export async function GET() {
  const quests = await prisma.quest.findMany({ include: { progress: true } });
  return NextResponse.json({ quests });
}
