export { default } from 'next-auth/middleware';

export const config = {
  matcher: ['/dashboard/:path*', '/announcements/:path*', '/progress/:path*', '/quests/:path*', '/badges/:path*', '/schedule/:path*', '/messages/:path*', '/uploads/:path*', '/help/:path*', '/admin/:path*']
};
