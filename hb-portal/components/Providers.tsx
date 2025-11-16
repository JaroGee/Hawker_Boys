'use client';

import { SessionProvider } from 'next-auth/react';
import type { ReactNode } from 'react';
import { ThemeProvider } from 'next-themes';
import { Toaster } from 'sonner';

export function Providers({ children }: { children: ReactNode }) {
  return (
    <SessionProvider>
      <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
        <Toaster position="top-right" richColors />
        {children}
      </ThemeProvider>
    </SessionProvider>
  );
}
