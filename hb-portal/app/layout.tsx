import './globals.css';
import type { ReactNode } from 'react';
import { Metadata } from 'next';
import { Providers } from '../components/Providers';

export const metadata: Metadata = {
  title: 'Hawker Boys Portal',
  description: 'Empowering trainees, mentors, and employers across Hawker Boys programmes.',
  icons: {
    icon: '/favicons/favicon-32x32.png'
  },
  openGraph: {
    title: 'Hawker Boys Portal',
    description: 'Role-based hub for training progress and operations',
    images: ['/og/main.svg']
  }
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="bg-surface-muted">
      <body className="font-sans text-ink">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
