import type { Metadata } from 'next';
import { Source_Sans_3 } from 'next/font/google';
import './globals.css';
import '@total-typescript/ts-reset';
import { Logo } from '@/components/logo';
import { GlobalNav } from '@/components/global-nav';

const sourceSans = Source_Sans_3({ subsets: ['latin'], variable: '--font-source-sans' });

export const metadata: Metadata = {
  title: 'Hawker Boys Portal',
  description: 'Role-aware PDPA-ready portal for trainees, mentors, employers, and administrators.',
  metadataBase: new URL(process.env.APP_BASE_URL ?? 'http://localhost:3000'),
  openGraph: {
    title: 'Hawker Boys Portal',
    description: 'Progress tracking, employer coordination, and care in one secure hub.',
    images: ['/og/default.svg']
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={sourceSans.variable}>
      <body className="min-h-screen bg-brand-muted/40">
        <header className="sticky top-0 z-20 border-b border-brand-muted bg-white/95 backdrop-blur">
          <div className="mx-auto flex max-w-6xl flex-col gap-4 px-6 py-4 md:flex-row md:items-center md:justify-between">
            <Logo />
            <GlobalNav />
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-6 py-10">
          {children}
        </main>
        <footer className="border-t border-brand-muted bg-white py-8 text-center text-sm text-slate-500">
          Hawker Boys © {new Date().getFullYear()} · PDPA-aligned training support
        </footer>
      </body>
    </html>
  );
}
