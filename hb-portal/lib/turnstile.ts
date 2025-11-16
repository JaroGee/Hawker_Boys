export async function validateTurnstileToken(token: string, ip?: string) {
  if (!process.env.TURNSTILE_SECRET_KEY) {
    return true;
  }
  const form = new URLSearchParams();
  form.append('secret', process.env.TURNSTILE_SECRET_KEY);
  form.append('response', token);
  if (ip) {
    form.append('remoteip', ip);
  }
  const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    body: form
  });
  const data = await res.json();
  return data.success === true;
}
