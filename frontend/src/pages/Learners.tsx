import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';

import { EmptyState } from '../components/EmptyState';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { PaginationControls } from '../components/PaginationControls';
import { useDebounce } from '../hooks/useDebounce';
import { fetchLearners } from '../lib/api';

const LearnersPage = () => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const debounced = useDebounce(search, 300);

  const learnersQuery = useQuery({
    queryKey: ['learners', page, debounced],
    queryFn: async () => {
      const response = await fetchLearners({ page, q: debounced, page_size: 10 });
      return response.data;
    },
    keepPreviousData: true,
  });

  if (learnersQuery.isLoading) return <LoadingState label="Loading learners" />;
  if (learnersQuery.isError)
    return (
      <ErrorState
        message="Unable to load learners."
        action={
          <button type="button" className="hb-button hb-button--primary" onClick={() => learnersQuery.refetch()}>
            Retry
          </button>
        }
      />
    );

  const learners = learnersQuery.data?.items ?? [];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Learners</h1>
          <p className="page-subtitle">People enrolled into Hawker Boys programmes.</p>
        </div>
      </div>
      <div className="card" style={{ marginBottom: 'var(--hb-space-lg)' }}>
        <input
          className="search-input"
          placeholder="Search by name or NRIC"
          value={search}
          onChange={(event) => {
            setSearch(event.target.value);
            setPage(1);
          }}
        />
      </div>
      <div className="card">
        {learners.length === 0 ? (
          <EmptyState title="No learners" description="Add learners via enrollments or import." />
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Masked NRIC</th>
                  <th>Contact</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {learners.map((learner) => (
                  <tr key={learner.id}>
                    <td>
                      {learner.given_name} {learner.family_name}
                    </td>
                    <td>{learner.masked_nric ?? '—'}</td>
                    <td>{learner.contact_number ?? '—'}</td>
                    <td>{new Date(learner.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <PaginationControls
              page={page}
              pageSize={10}
              total={learnersQuery.data?.total ?? 0}
              onPrevious={() => setPage((prev) => Math.max(1, prev - 1))}
              onNext={() => setPage((prev) => prev + 1)}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default LearnersPage;
