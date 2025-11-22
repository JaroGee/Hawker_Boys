const nextSafe = require('next-safe');

const securityHeaders = nextSafe({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", 'https://challenges.cloudflare.com'],
      imgSrc: ["'self'", 'data:', 'https:'],
      styleSrc: ["'self'", "'unsafe-inline'"],
      connectSrc: ["'self'", 'https://challenges.cloudflare.com'],
      frameSrc: ['https://challenges.cloudflare.com'],
      objectSrc: ["'none'"],
      baseUri: ["'self'"],
      formAction: ["'self'"]
    }
  },
  isDev: process.env.NODE_ENV !== 'production'
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    typedRoutes: true
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**'
      }
    ]
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: securityHeaders
      }
    ];
  }
};

module.exports = nextConfig;
