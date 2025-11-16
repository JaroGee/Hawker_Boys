import { canAccess, type UserRole } from '@/lib/auth/roles';

export function assertRole(userRole: UserRole | undefined | null, required: UserRole) {
  if (!canAccess(required, userRole ?? undefined)) {
    throw new Error('Forbidden');
  }
}
