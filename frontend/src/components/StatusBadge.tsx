type Props = {
  label: string;
  tone?: 'accent' | 'success' | 'danger';
};

export const StatusBadge = ({ label, tone = 'accent' }: Props) => (
  <span className={`badge badge--${tone}`}>{label}</span>
);
