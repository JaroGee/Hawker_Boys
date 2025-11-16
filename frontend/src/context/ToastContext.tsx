import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

type ToastTone = 'info' | 'success' | 'error';

export type ToastPayload = {
  title: string;
  description?: string;
  tone?: ToastTone;
  durationMs?: number;
};

type ToastRecord = ToastPayload & { id: string };

type ToastContextValue = {
  push: (payload: ToastPayload) => void;
  dismiss: (id: string) => void;
};

const ToastContext = createContext<ToastContextValue | undefined>(undefined);

const generateId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return Math.random().toString(36).slice(2);
};

const ToastStack = ({ toasts, onDismiss }: { toasts: ToastRecord[]; onDismiss: (id: string) => void }) => {
  return (
    <div className="toast-stack">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast--${toast.tone ?? 'info'}`}>
          <strong>{toast.title}</strong>
          {toast.description && <p>{toast.description}</p>}
          <button type="button" className="hb-button hb-button--ghost" onClick={() => onDismiss(toast.id)}>
            Dismiss
          </button>
        </div>
      ))}
    </div>
  );
};

export const ToastProvider = ({ children }: { children: React.ReactNode }) => {
  const [toasts, setToasts] = useState<ToastRecord[]>([]);
  const containerRef = useRef<Element | null>(null);

  useEffect(() => {
    containerRef.current = document.getElementById('toast-root');
  }, []);

  const dismiss = useCallback((id: string) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  }, []);

  const push = useCallback(
    (payload: ToastPayload) => {
      const toast: ToastRecord = { ...payload, id: generateId() };
      setToasts((current) => [...current, toast]);
      const duration = payload.durationMs ?? 4500;
      if (duration > 0) {
        setTimeout(() => dismiss(toast.id), duration);
      }
    },
    [dismiss],
  );

  const value = useMemo(() => ({ push, dismiss }), [dismiss, push]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      {containerRef.current && createPortal(<ToastStack toasts={toasts} onDismiss={dismiss} />, containerRef.current)}
    </ToastContext.Provider>
  );
};

export const useToast = (): ToastContextValue => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
};
