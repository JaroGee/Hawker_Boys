import type { UserProfile } from '../types/api';

const TOKEN_KEY = 'hb.tms.token';
const PROFILE_KEY = 'hb.tms.profile';
const REMEMBER_KEY = 'hb.tms.remember';

const safeStorage = (storage: Storage) => {
  try {
    const testKey = '__hb_test__';
    storage.setItem(testKey, 'ok');
    storage.removeItem(testKey);
    return storage;
  } catch {
    return null;
  }
};

const local = typeof window !== 'undefined' ? safeStorage(window.localStorage) : null;
const session = typeof window !== 'undefined' ? safeStorage(window.sessionStorage) : null;

const getFromStores = (key: string): string | null => {
  return local?.getItem(key) ?? session?.getItem(key) ?? null;
};

const removeFromStores = (key: string) => {
  local?.removeItem(key);
  session?.removeItem(key);
};

export const authStorage = {
  persistSession(token: string, profile: UserProfile, remember: boolean) {
    const target = authStorage.storeToken(token, remember);
    if (!target) return;
    removeFromStores(PROFILE_KEY);
    target.setItem(PROFILE_KEY, JSON.stringify(profile));
    if (remember) {
      local?.setItem(REMEMBER_KEY, '1');
    } else {
      local?.removeItem(REMEMBER_KEY);
    }
  },
  storeToken(token: string, remember: boolean) {
    const target = remember ? local : session;
    if (!target) return null;
    removeFromStores(TOKEN_KEY);
    target.setItem(TOKEN_KEY, token);
    if (remember) {
      local?.setItem(REMEMBER_KEY, '1');
    } else {
      local?.removeItem(REMEMBER_KEY);
    }
    return target;
  },
  getToken(): string | null {
    return getFromStores(TOKEN_KEY);
  },
  getProfile(): UserProfile | null {
    const raw = getFromStores(PROFILE_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw) as UserProfile;
    } catch {
      return null;
    }
  },
  wasRemembered(): boolean {
    return local?.getItem(REMEMBER_KEY) === '1';
  },
  clear() {
    removeFromStores(TOKEN_KEY);
    removeFromStores(PROFILE_KEY);
    local?.removeItem(REMEMBER_KEY);
  },
};
