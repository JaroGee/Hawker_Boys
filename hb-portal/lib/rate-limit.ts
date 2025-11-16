const buckets = new Map<string, { count: number; expiresAt: number }>();

export async function isRateLimited(key: string, limit = 5, windowMs = 60_000) {
  const now = Date.now();
  const existing = buckets.get(key);
  if (existing && existing.expiresAt > now) {
    if (existing.count >= limit) {
      return true;
    }
    existing.count += 1;
    return false;
  }
  buckets.set(key, { count: 1, expiresAt: now + windowMs });
  return false;
}
