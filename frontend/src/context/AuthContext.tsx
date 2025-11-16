import { createContext, useContext, useEffect, useMemo, useState } from 'react';

import { loginRequest, meRequest } from '../lib/api';
import { authStorage } from '../lib/authStorage';
import type { LoginPayload, TokenResponse, UserProfile } from '../types/api';
import { useToast } from './ToastContext';

type AuthContextValue = {
  profile: UserProfile | null;
  token: string | null;
  initializing: boolean;
  login: (payload: LoginPayload & { remember: boolean }) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

type Props = {
  children: React.ReactNode;
};

export const AuthProvider = ({ children }: Props) => {
  const [token, setToken] = useState<string | null>(() => authStorage.getToken());
  const [profile, setProfile] = useState<UserProfile | null>(() => authStorage.getProfile());
  const [initializing, setInitializing] = useState(true);
  const toast = useToast();

  const hydrateSession = async (accessToken: string) => {
    try {
      const { data } = await meRequest();
      authStorage.persistSession(accessToken, data, authStorage.wasRemembered());
      setProfile(data);
    } catch (error) {
      authStorage.clear();
      setProfile(null);
      setToken(null);
    } finally {
      setInitializing(false);
    }
  };

  useEffect(() => {
    if (token && !profile) {
      hydrateSession(token);
    } else {
      setInitializing(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = async ({ email, password, remember }: LoginPayload & { remember: boolean }) => {
    const response = await loginRequest({ email, password });
    await hydrateAfterLogin(response.data, remember);
    toast.push({
      title: 'Signed in',
      description: `Welcome back ${response.data.role === 'admin' ? 'Admin' : ''}`,
      tone: 'success',
    });
  };

  const hydrateAfterLogin = async (tokenResponse: TokenResponse, remember: boolean) => {
    setToken(tokenResponse.access_token);
    const profileResponse = await meRequest();
    authStorage.persistSession(tokenResponse.access_token, profileResponse.data, remember);
    setProfile(profileResponse.data);
    setInitializing(false);
  };

  const logout = () => {
    authStorage.clear();
    setProfile(null);
    setToken(null);
  };

  const value = useMemo(
    () => ({
      profile,
      token,
      initializing,
      login,
      logout,
    }),
    [profile, token, initializing],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
