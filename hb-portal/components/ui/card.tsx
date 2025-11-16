import * as React from 'react';
import { cn } from '@/lib/utils';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, ...props }: CardProps) {
  return <div className={cn('rounded-xl border border-brand-muted/70 bg-white p-6 shadow-sm', className)} {...props} />;
}

export function CardHeader({ className, ...props }: CardProps) {
  return <div className={cn('mb-4 flex flex-col gap-2', className)} {...props} />;
}

export function CardTitle({ className, ...props }: CardProps) {
  return <h3 className={cn('font-display text-lg font-semibold text-brand-dark', className)} {...props} />;
}

export function CardDescription({ className, ...props }: CardProps) {
  return <p className={cn('text-sm text-slate-600', className)} {...props} />;
}
