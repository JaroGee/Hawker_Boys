import { randomUUID } from 'node:crypto';
import { prisma } from '@/lib/prisma';

export async function requestLiveLocation(traineeId: string, requestedByUserId: string, durationMinutes = 15) {
  const token = randomUUID();
  const expiresAt = new Date(Date.now() + durationMinutes * 60 * 1000);
  return prisma.liveLocationSession.create({
    data: { traineeId, requestedByUserId, token, expiresAt, active: false }
  });
}

export async function activateSession(token: string) {
  return prisma.liveLocationSession.update({
    where: { token },
    data: { active: true }
  });
}

export async function closeSession(token: string) {
  return prisma.liveLocationSession.update({
    where: { token },
    data: { active: false }
  });
}
