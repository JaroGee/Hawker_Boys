import { NextResponse } from 'next/server';
import { getSession } from '../../../lib/auth/session';
import { requireRole } from '../../../lib/rbac';
import { prisma } from '../../../lib/db';
import { Role } from '@prisma/client';

export async function GET() {
  const announcements = await prisma.announcement.findMany({
    orderBy: { publishedAt: 'desc' },
    take: 20
  });
  return NextResponse.json({ announcements });
}

export async function POST(request: Request) {
  const session = await getSession();
  requireRole(session?.user?.role as Role | undefined, [Role.ADMIN]);
  const body = await request.json();
  const announcement = await prisma.announcement.create({
    data: {
      title: body.title,
      body: body.body,
      audience: body.audience ?? 'ALL',
      authorId: session?.user?.id
    }
  });
  return NextResponse.json(announcement, { status: 201 });
}
