'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';

const NAV_ITEMS = [
  { label: 'Home', href: '/' },
  { label: 'Announcements', href: '/announcements' },
  { label: 'My Progress', href: '/progress' },
  { label: 'Quests', href: '/quests' },
  { label: 'Badges', href: '/badges' },
  { label: 'Schedule', href: '/schedule' },
  { label: 'Messages', href: '/messages' },
  { label: 'Uploads', href: '/uploads' },
  { label: 'Help', href: '/help' }
];

export function GlobalNav() {
  const pathname = usePathname();
  return (
    <nav className="flex flex-wrap items-center gap-4 text-sm">
      {NAV_ITEMS.map((item) => (
        <Link key={item.href} href={item.href} className={cn('transition-colors hover:text-brand-primary', pathname === item.href ? 'text-brand-primary font-semibold' : 'text-slate-600')}>
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
