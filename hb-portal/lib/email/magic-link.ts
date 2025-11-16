import type { SendVerificationRequestParams } from 'next-auth/providers/email';

export async function sendMagicLink({ identifier, url, provider }: SendVerificationRequestParams) {
  const subject = 'Your secure Hawker Boys login link';
  const body = `Hi there,\n\nClick the button below to complete your sign in.\n${url}\n\nThis link expires in 10 minutes.`;

  if (process.env.RESEND_API_KEY) {
    const endpoint = 'https://api.resend.com/emails';
    await fetch(endpoint, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ from: provider.from ?? 'portal@hawkerboys.com', to: identifier, subject, text: body })
    });
    return;
  }

  if (process.env.POSTMARK_API_TOKEN) {
    await fetch('https://api.postmarkapp.com/email', {
      method: 'POST',
      headers: {
        'X-Postmark-Server-Token': process.env.POSTMARK_API_TOKEN,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ From: provider.from ?? 'portal@hawkerboys.com', To: identifier, Subject: subject, TextBody: body })
    });
    return;
  }

  console.info('[magic-link]', identifier, url);
}
