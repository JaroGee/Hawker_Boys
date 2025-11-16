import { prisma } from '@/lib/prisma';
import type { UserRole } from '@/lib/auth/roles';

export async function recordAudit(action: string, actorRole: UserRole, entity: string, entityId?: string, meta?: Record<string, unknown>) {
  await prisma.auditEvent.create({
    data: {
      action,
      actorRole,
      entity,
      entityId,
      meta
    }
  });
}
