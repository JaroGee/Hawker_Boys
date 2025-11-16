export const LoadingState = ({ label = 'Loading' }: { label?: string }) => (
  <div className="empty-state">
    <div className="empty-state__illustration" aria-hidden="true">
      ⏳
    </div>
    <p>{label}…</p>
  </div>
);
