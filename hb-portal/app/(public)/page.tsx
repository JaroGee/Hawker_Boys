import Link from 'next/link';
import Image from 'next/image';

export default function LandingPage() {
  return (
    <main className="bg-surface-muted">
      <section className="mx-auto flex min-h-screen max-w-5xl flex-col items-center justify-center gap-10 px-6 py-24 text-center">
        <Image src="/favicons/portal-mark.svg" alt="Hawker Boys" width={120} height={120} />
        <h1 className="text-4xl font-bold text-ink">
          Hawker Boys Portal keeps the flame burning for every trainee, mentor, and employer.
        </h1>
        <p className="max-w-2xl text-lg text-ink-subtle">
          Log shifts, track WSQ progression, cheer on achievements, and rally help quickly. Built with the warmth of our hawker
          community and the rigour our trainees deserve.
        </p>
        <div className="flex flex-col items-center gap-3 sm:flex-row">
          <Link
            href="/login"
            className="rounded-full bg-brand px-6 py-3 text-sm font-semibold uppercase tracking-wide text-white shadow-sm transition hover:bg-brand-dark"
          >
            Sign in to the portal
          </Link>
          <Link
            href="/public/feedback"
            className="rounded-full border border-brand px-6 py-3 text-sm font-semibold uppercase tracking-wide text-brand transition hover:bg-brand/10"
          >
            Leave feedback for a trainee
          </Link>
        </div>
      </section>
    </main>
  );
}
