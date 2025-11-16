import { describe, expect, it } from 'vitest';
import { canAccess } from '@/lib/auth/roles';

describe('canAccess', () => {
  it('enforces hierarchy', () => {
    expect(canAccess('MENTOR', 'ADMIN')).toBe(true);
    expect(canAccess('ADMIN', 'MENTOR')).toBe(false);
  });
});
