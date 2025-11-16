type Props = {
  message?: string;
  action?: React.ReactNode;
};

export const ErrorState = ({ message, action }: Props) => (
  <div className="empty-state">
    <div className="empty-state__illustration" aria-hidden="true">
      ⚠️
    </div>
    <h3>Something went wrong</h3>
    {message && <p>{message}</p>}
    {action}
  </div>
);
