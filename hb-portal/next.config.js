/** @type {import('next').NextConfig} */
const securityHeaders = async () => {
  const { createHeaders } = await import('next-safe');
  return createHeaders({
    contentSecurityPolicy: {
      "default-src": ["'self'"],
      "script-src": ["'self'", "https://challenges.cloudflare.com"],
      "style-src": ["'self'", "'unsafe-inline'"],
      "img-src": ["'self'", 'data:', 'blob:'],
      "connect-src": ["'self'", process.env.NEXT_PUBLIC_API_BASE ?? "'self'"],
      "font-src": ["'self'"],
      "frame-src": ["'self'", "https://challenges.cloudflare.com"],
      upgradeInsecureRequests: true
    },
    referrerPolicy: 'strict-origin-when-cross-origin',
    permissionsPolicy: {
      camera: ['none'],
      microphone: ['none'],
      geolocation: ['self']
    }
  });
};

const nextConfig = {
  reactStrictMode: true,
  experimental: {
    typedRoutes: true,
    serverActions: true
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: await securityHeaders()
      }
    ];
  }
};

module.exports = nextConfig;
