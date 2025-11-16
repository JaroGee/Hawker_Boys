type DrawerProps = {
  title: string;
  description?: string;
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
};

export const Drawer = ({ title, description, isOpen, onClose, children }: DrawerProps) => {
  if (!isOpen) return null;
  return (
    <div className="drawer-backdrop" role="dialog" aria-modal="true" aria-label={title}>
      <div className="drawer">
        <header className="page-header">
          <div>
            <h2 className="page-title">{title}</h2>
            {description && <p className="page-subtitle">{description}</p>}
          </div>
          <button type="button" className="hb-button hb-button--ghost" onClick={onClose}>
            Close
          </button>
        </header>
        {children}
      </div>
    </div>
  );
};
