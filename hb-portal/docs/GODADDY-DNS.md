# GoDaddy DNS & Navigation

1. In GoDaddy DNS for hawkerboys.com create a CNAME record:
   - Name: `portal`
   - Value: `cname.vercel-dns.com`
   - TTL: 1 hour
2. In Vercel project settings add `portal.hawkerboys.com` as a custom domain.
3. Once propagated, update GoDaddy Website Builder navigation:
   - Settings → Site Navigation
   - Add a new nav item labelled **Portal** linking to `https://portal.hawkerboys.com`
4. Optional embed of the public feedback page:
   - Add an iframe block pointing to `https://portal.hawkerboys.com/public/feedback`
   - Enable `Allow` for clipboard + scripts so Cloudflare Turnstile loads
