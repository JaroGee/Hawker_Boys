import { PrismaAdapter } from '@next-auth/prisma-adapter';
import type { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import EmailProvider from 'next-auth/providers/email';
import { compare } from 'bcryptjs';
import { prisma } from '@/lib/prisma';
import { sendMagicLink } from '@/lib/email/magic-link';
import type { UserRole } from './roles';

export const authOptions: NextAuthOptions = {
  adapter: PrismaAdapter(prisma),
  session: { strategy: 'jwt' },
  pages: {
    signIn: '/auth/sign-in'
  },
  providers: [
    CredentialsProvider({
      name: 'Admin Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;
        const user = await prisma.user.findUnique({ where: { email: credentials.email } });
        if (!user || user.role !== 'ADMIN' || !user.passwordHash) {
          return null;
        }
        const match = await compare(credentials.password, user.passwordHash);
        if (!match) return null;
        return { id: user.id, email: user.email, role: user.role } as any;
      }
    }),
    EmailProvider({
      from: 'portal@hawkerboys.com',
      maxAge: 10 * 60,
      async sendVerificationRequest(params) {
        return sendMagicLink(params);
      }
    })
  ],
  callbacks: {
    async signIn({ user, account }) {
      if (account?.provider === 'email' && user?.role === 'ADMIN') {
        return false;
      }
      return true;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.sub as string;
        session.user.role = token.role as UserRole;
      }
      return session;
    },
    async jwt({ token, user }) {
      if (user) {
        token.role = (user as any).role ?? 'TRAINEE';
      }
      return token;
    }
  }
};
