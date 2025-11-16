type Props = {
  page: number;
  pageSize: number;
  total: number;
  onPrevious: () => void;
  onNext: () => void;
};

export const PaginationControls = ({ page, pageSize, total, onPrevious, onNext }: Props) => {
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  return (
    <div className="pagination">
      <div>
        Showing {(page - 1) * pageSize + 1} - {Math.min(page * pageSize, total)} of {total}
      </div>
      <div className="input-group">
        <button type="button" className="hb-button hb-button--secondary" onClick={onPrevious} disabled={page <= 1}>
          Previous
        </button>
        <span className="chip">
          Page {page} of {totalPages}
        </span>
        <button
          type="button"
          className="hb-button hb-button--secondary"
          onClick={onNext}
          disabled={page >= totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
};
