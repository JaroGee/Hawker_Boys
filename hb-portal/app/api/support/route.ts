import { NextResponse } from 'next/server';
import { z } from 'zod';
import { prisma } from '@/lib/prisma';

const schema = z.object({ traineeId: z.string().optional(), message: z.string().min(5), category: z.string().default('GENERAL') });

export async function POST(req: Request) {
  const payload = schema.parse(await req.json());
  const ticket = await prisma.supportTicket.create({ data: { traineeId: payload.traineeId, message: payload.message, category: payload.category } });
  return NextResponse.json(ticket);
}
