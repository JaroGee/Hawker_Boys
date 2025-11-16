import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function POST(request: Request, { params }: { params: { token: string } }) {
  const body = await request.json();
  const session = await prisma.liveLocationSession.findUnique({ where: { token: params.token } });
  if (!session || !session.active) {
    return NextResponse.json({ message: 'Session inactive' }, { status: 400 });
  }
  await prisma.liveLocationPing.create({
    data: {
      sessionId: session.id,
      lat: body.lat,
      lng: body.lng,
      accuracy: body.accuracy,
      at: new Date()
    }
  });
  return NextResponse.json({ ok: true });
}
