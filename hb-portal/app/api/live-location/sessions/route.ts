import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { z } from 'zod';
import { authOptions } from '@/lib/auth/options';
import { assertRole } from '@/lib/rbac';
import { requestLiveLocation } from '@/lib/live-location';

const schema = z.object({ traineeId: z.string(), durationMinutes: z.coerce.number().min(5).max(60) });

export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  assertRole(session?.user.role, 'MENTOR');
  const body = schema.parse(await req.json());
  const record = await requestLiveLocation(body.traineeId, session!.user.id, body.durationMinutes);
  return NextResponse.json(record);
}
