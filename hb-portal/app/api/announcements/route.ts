import { NextResponse } from 'next/server';
import { z } from 'zod';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth/options';
import { prisma } from '@/lib/prisma';
import { assertRole } from '@/lib/rbac';

const bodySchema = z.object({
  title: z.string().min(2),
  body: z.string().min(4),
  audience: z.enum(['ALL', 'TRAINEES', 'MENTORS', 'EMPLOYERS'])
});

export async function GET() {
  const announcements = await prisma.announcement.findMany({ orderBy: { publishedAt: 'desc' }, take: 50 });
  return NextResponse.json(announcements);
}

export async function POST(request: Request) {
  const session = await getServerSession(authOptions);
  assertRole(session?.user.role, 'ADMIN');
  const json = await request.json();
  const data = bodySchema.parse(json);
  const announcement = await prisma.announcement.create({ data: { ...data, publishedAt: new Date() } });
  return NextResponse.json(announcement);
}
