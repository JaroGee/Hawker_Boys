interface LogoProps {
  className?: string;
}

export function Logo({ className }: LogoProps) {
  return (
    <div className={`flex items-center gap-2 font-display text-xl font-bold text-brand-primary ${className ?? ''}`}>
      <span role="img" aria-label="flame" className="text-3xl">
        🍜
      </span>
      <span>Hawker Boys Portal</span>
    </div>
  );
}
