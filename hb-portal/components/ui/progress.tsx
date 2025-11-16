import * as React from 'react';

export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value: number;
}

export function Progress({ value, ...props }: ProgressProps) {
  const width = Math.min(100, Math.max(0, value));
  return (
    <div className="w-full rounded-full bg-brand-muted/60" {...props}>
      <div className="h-3 rounded-full bg-brand-primary transition-all" style={{ width: `${width}%` }} />
    </div>
  );
}
