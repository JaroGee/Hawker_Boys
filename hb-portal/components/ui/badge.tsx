import { cn } from '@/lib/utils';

export function Badge({ label, className }: { label: string; className?: string }) {
  return <span className={cn('inline-flex rounded-full bg-brand-muted px-3 py-1 text-xs font-semibold text-brand-dark', className)}>{label}</span>;
}
