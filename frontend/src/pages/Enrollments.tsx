import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';

import { EmptyState } from '../components/EmptyState';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { PaginationControls } from '../components/PaginationControls';
import { StatusBadge } from '../components/StatusBadge';
import { useDebounce } from '../hooks/useDebounce';
import { fetchEnrollments } from '../lib/api';

const EnrollmentsPage = () => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const debounced = useDebounce(search, 300);

  const enrollmentsQuery = useQuery({
    queryKey: ['enrollments', page, debounced],
    queryFn: async () => {
      const response = await fetchEnrollments({ page, q: debounced, page_size: 10 });
      return response.data;
    },
    keepPreviousData: true,
  });

  if (enrollmentsQuery.isLoading) return <LoadingState label="Loading enrollments" />;
  if (enrollmentsQuery.isError)
    return (
      <ErrorState
        message="Unable to load enrollments."
        action={
          <button type="button" className="hb-button hb-button--primary" onClick={() => enrollmentsQuery.refetch()}>
            Retry
          </button>
        }
      />
    );

  const enrollments = enrollmentsQuery.data?.items ?? [];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Enrollments</h1>
          <p className="page-subtitle">Learners linked to class runs.</p>
        </div>
      </div>
      <div className="card" style={{ marginBottom: 'var(--hb-space-lg)' }}>
        <input
          className="search-input"
          placeholder="Search by learner or class reference"
          value={search}
          onChange={(event) => {
            setSearch(event.target.value);
            setPage(1);
          }}
        />
      </div>
      <div className="card">
        {enrollments.length === 0 ? (
          <EmptyState title="No enrollments" description="Create a class run and add learners into it." />
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Enrollment ID</th>
                  <th>Learner ID</th>
                  <th>Class run</th>
                  <th>Status</th>
                  <th>Enrolled</th>
                </tr>
              </thead>
              <tbody>
                {enrollments.map((enrollment) => (
                  <tr key={enrollment.id}>
                    <td>{enrollment.id.slice(0, 8)}</td>
                    <td>{enrollment.learner_id.slice(0, 8)}</td>
                    <td>{enrollment.class_run_id.slice(0, 8)}</td>
                    <td>
                      <StatusBadge
                        label={enrollment.status.replace('_', ' ')}
                        tone={
                          enrollment.status === 'completed'
                            ? 'success'
                            : enrollment.status === 'withdrawn'
                            ? 'danger'
                            : 'accent'
                        }
                      />
                    </td>
                    <td>{new Date(enrollment.enrollment_date).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <PaginationControls
              page={page}
              pageSize={10}
              total={enrollmentsQuery.data?.total ?? 0}
              onPrevious={() => setPage((prev) => Math.max(1, prev - 1))}
              onNext={() => setPage((prev) => prev + 1)}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default EnrollmentsPage;
