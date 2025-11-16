import { NextResponse } from 'next/server';
import { getSession } from '../../../lib/auth/session';
import { prisma } from '../../../lib/db';

export async function POST(request: Request) {
  const session = await getSession();
  if (!session?.user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  const body = await request.json();
  const sessionRecord = await prisma.liveLocationSession.update({
    where: { token: body.token },
    data: {
      active: body.active,
      pings: body.ping
        ? {
            create: {
              lat: body.ping.lat,
              lng: body.ping.lng,
              accuracy: body.ping.accuracy
            }
          }
        : undefined
    }
  });
  return NextResponse.json(sessionRecord);
}
