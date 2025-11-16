type Props = {
  label: string;
  htmlFor: string;
  children: React.ReactNode;
  hint?: string;
};

export const FormField = ({ label, htmlFor, children, hint }: Props) => (
  <div className="form-field">
    <label htmlFor={htmlFor}>{label}</label>
    {children}
    {hint && <small className="page-subtitle">{hint}</small>}
  </div>
);
