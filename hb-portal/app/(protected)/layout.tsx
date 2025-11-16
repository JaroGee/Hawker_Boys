import { redirect } from 'next/navigation';
import { ReactNode } from 'react';
import { getSession } from '../../lib/auth/session';
import { PortalShell } from '../../components/layout/PortalShell';

export default async function ProtectedLayout({ children }: { children: ReactNode }) {
  const session = await getSession();
  if (!session?.user) {
    redirect('/login');
  }
  return <PortalShell role={session.user.role}>{children}</PortalShell>;
}
