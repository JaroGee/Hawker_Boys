import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';

import { EmptyState } from '../components/EmptyState';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { PaginationControls } from '../components/PaginationControls';
import { StatusBadge } from '../components/StatusBadge';
import { useDebounce } from '../hooks/useDebounce';
import { fetchClassRuns } from '../lib/api';

const ClassRunsPage = () => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const debounced = useDebounce(search, 300);

  const runsQuery = useQuery({
    queryKey: ['class-runs', page, debounced],
    queryFn: async () => {
      const response = await fetchClassRuns({ page, q: debounced, page_size: 10 });
      return response.data;
    },
    keepPreviousData: true,
  });

  if (runsQuery.isLoading) return <LoadingState label="Loading class runs" />;
  if (runsQuery.isError)
    return (
      <ErrorState
        message="Unable to load class runs."
        action={
          <button type="button" className="hb-button hb-button--primary" onClick={() => runsQuery.refetch()}>
            Retry
          </button>
        }
      />
    );

  const runs = runsQuery.data?.items ?? [];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Class Runs</h1>
          <p className="page-subtitle">Scheduling, status, and sync visibility.</p>
        </div>
      </div>
      <div className="card" style={{ marginBottom: 'var(--hb-space-lg)' }}>
        <input
          className="search-input"
          placeholder="Filter by reference or course"
          value={search}
          onChange={(event) => {
            setSearch(event.target.value);
            setPage(1);
          }}
        />
      </div>
      <div className="card">
        {runs.length === 0 ? (
          <EmptyState title="No runs yet" description="Publish a run from the course view to see it here." />
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Reference</th>
                  <th>Course</th>
                  <th>Status</th>
                  <th>Schedule</th>
                </tr>
              </thead>
              <tbody>
                {runs.map((run) => (
                  <tr key={run.id}>
                    <td>{run.reference_code}</td>
                    <td>{run.course_title}</td>
                    <td>
                      <StatusBadge
                        label={run.status}
                        tone={run.status === 'published' ? 'success' : run.status === 'cancelled' ? 'danger' : 'accent'}
                      />
                    </td>
                    <td>
                      {new Date(run.start_date).toLocaleDateString()} – {new Date(run.end_date).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <PaginationControls
              page={page}
              pageSize={10}
              total={runsQuery.data?.total ?? 0}
              onPrevious={() => setPage((prev) => Math.max(1, prev - 1))}
              onNext={() => setPage((prev) => prev + 1)}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default ClassRunsPage;
