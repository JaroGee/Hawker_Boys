import { redirect } from 'next/navigation';
import { getSession } from '../../../lib/auth/session';
import { LoginCard } from '../../../components/auth/LoginCard';

export default async function LoginPage() {
  const session = await getSession();
  if (session?.user) {
    redirect('/dashboard');
  }
  return <LoginCard />;
}
