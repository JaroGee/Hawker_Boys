export type UserRole = 'TRAINEE' | 'MENTOR' | 'EMPLOYER' | 'ADMIN';

export const roleHierarchy: Record<UserRole, number> = {
  TRAINEE: 0,
  EMPLOYER: 1,
  MENTOR: 2,
  ADMIN: 3
};

export function canAccess(required: UserRole, actual?: UserRole | null) {
  if (!actual) return false;
  return roleHierarchy[actual] >= roleHierarchy[required];
}

export const dashboardRoutes: Record<UserRole, string> = {
  TRAINEE: '/dashboard/trainee',
  MENTOR: '/dashboard/mentor',
  EMPLOYER: '/dashboard/employer',
  ADMIN: '/dashboard/admin'
};
