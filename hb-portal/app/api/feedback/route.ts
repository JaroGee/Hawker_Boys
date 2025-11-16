import { NextResponse } from 'next/server';
import { headers } from 'next/headers';
import { prisma } from '../../../lib/db';
import { verifyTurnstile } from '../../../lib/turnstile';
import { rateLimit } from '../../../lib/rate-limit';

export async function GET() {
  const feedback = await prisma.customerFeedback.findMany({
    orderBy: { createdAt: 'desc' },
    take: 50,
    include: {
      trainee: { select: { name: true } }
    }
  });
  return NextResponse.json({ feedback });
}

export async function POST(request: Request) {
  const body = await request.json();
  const ip = headers().get('x-forwarded-for') ?? headers().get('x-real-ip') ?? undefined;
  if (!rateLimit(ip ?? 'public')) {
    return NextResponse.json({ error: 'Too many submissions' }, { status: 429 });
  }
  const turnstileValid = await verifyTurnstile(body.turnstileToken ?? null, ip);
  if (!turnstileValid) {
    return NextResponse.json({ error: 'Turnstile validation failed' }, { status: 400 });
  }
  const trainee = await prisma.traineeProfile.findUnique({ where: { userId: body.traineeId } });
  if (!trainee) {
    return NextResponse.json({ error: 'Trainee not found' }, { status: 404 });
  }
  const record = await prisma.customerFeedback.create({
    data: {
      traineeId: trainee.userId,
      rating: body.rating,
      comment: body.comment,
      receiptCode: body.receiptCode,
      meta: body.meta ?? {}
    }
  });
  return NextResponse.json(record, { status: 201 });
}
