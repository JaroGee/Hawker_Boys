'use client';

import { useEffect, useRef } from 'react';

interface Props {
  siteKey?: string;
  onVerify(token: string): void;
}

export function Turnstile({ siteKey, onVerify }: Props) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!siteKey || typeof window === 'undefined') return;
    const win = window as any;
    const renderWidget = () => {
      if (!ref.current || !win.turnstile) return;
      win.turnstile.render(ref.current, {
        sitekey: siteKey,
        callback: onVerify,
        theme: 'light'
      });
    };
    if (win.turnstile) {
      renderWidget();
    } else {
      const script = document.createElement('script');
      script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js';
      script.async = true;
      script.onload = renderWidget;
      document.body.appendChild(script);
    }
  }, [siteKey, onVerify]);

  if (!siteKey) {
    return <p className="text-sm text-slate-500">Turnstile disabled in dev. Token logged to console.</p>;
  }

  return <div ref={ref} />;
}
