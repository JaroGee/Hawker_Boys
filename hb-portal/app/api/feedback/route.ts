import { NextResponse } from 'next/server';
import { z } from 'zod';
import { prisma } from '@/lib/prisma';
import { validateTurnstileToken } from '@/lib/turnstile';
import { isRateLimited } from '@/lib/rate-limit';

const schema = z.object({
  traineeId: z.string().min(1),
  rating: z.coerce.number().min(1).max(5),
  comment: z.string().min(5),
  receiptCode: z.string().optional(),
  turnstileToken: z.string()
});

export async function POST(request: Request) {
  const ip = request.headers.get('x-forwarded-for') ?? 'unknown';
  if (await isRateLimited(`feedback:${ip}`, 5, 15 * 60 * 1000)) {
    return NextResponse.json({ message: 'Too many submissions' }, { status: 429 });
  }
  const body = await request.json();
  const payload = schema.parse(body);
  const isHuman = await validateTurnstileToken(payload.turnstileToken, ip);
  if (!isHuman) {
    return NextResponse.json({ message: 'Verification failed' }, { status: 400 });
  }
  const feedback = await prisma.customerFeedback.create({
    data: {
      traineeId: payload.traineeId,
      rating: payload.rating,
      comment: payload.comment,
      receiptCode: payload.receiptCode,
      meta: { ip }
    }
  });
  return NextResponse.json(feedback);
}
