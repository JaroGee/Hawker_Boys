type Props = {
  title: string;
  description?: string;
  action?: React.ReactNode;
};

export const EmptyState = ({ title, description, action }: Props) => (
  <div className="empty-state">
    <div className="empty-state__illustration" aria-hidden="true">
      🍜
    </div>
    <h3>{title}</h3>
    {description && <p>{description}</p>}
    {action}
  </div>
);
