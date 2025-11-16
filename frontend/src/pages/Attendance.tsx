import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';

import { EmptyState } from '../components/EmptyState';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { PaginationControls } from '../components/PaginationControls';
import { StatusBadge } from '../components/StatusBadge';
import { useDebounce } from '../hooks/useDebounce';
import { fetchAttendance } from '../lib/api';

const AttendancePage = () => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const debounced = useDebounce(search, 300);

  const attendanceQuery = useQuery({
    queryKey: ['attendance', page, debounced],
    queryFn: async () => {
      const response = await fetchAttendance({ page, q: debounced, page_size: 10 });
      return response.data;
    },
    keepPreviousData: true,
  });

  if (attendanceQuery.isLoading) return <LoadingState label="Loading attendance" />;
  if (attendanceQuery.isError)
    return (
      <ErrorState
        message="Unable to load attendance records."
        action={
          <button type="button" className="hb-button hb-button--primary" onClick={() => attendanceQuery.refetch()}>
            Retry
          </button>
        }
      />
    );

  const records = attendanceQuery.data?.items ?? [];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Attendance</h1>
          <p className="page-subtitle">Session-level acknowledgement.</p>
        </div>
      </div>
      <div className="card" style={{ marginBottom: 'var(--hb-space-lg)' }}>
        <input
          className="search-input"
          placeholder="Search by enrollment or session"
          value={search}
          onChange={(event) => {
            setSearch(event.target.value);
            setPage(1);
          }}
        />
      </div>
      <div className="card">
        {records.length === 0 ? (
          <EmptyState title="No attendance" description="Mark attendance from the trainer console." />
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Enrollment</th>
                  <th>Session</th>
                  <th>Status</th>
                  <th>Submitted</th>
                </tr>
              </thead>
              <tbody>
                {records.map((record) => (
                  <tr key={record.id}>
                    <td>{record.enrollment_id.slice(0, 8)}</td>
                    <td>{record.session_id.slice(0, 8)}</td>
                    <td>
                      <StatusBadge
                        label={record.status}
                        tone={record.status === 'present' ? 'success' : record.status === 'absent' ? 'danger' : 'accent'}
                      />
                    </td>
                    <td>{record.submitted_to_ssg ? 'Synced' : 'Pending'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <PaginationControls
              page={page}
              pageSize={10}
              total={attendanceQuery.data?.total ?? 0}
              onPrevious={() => setPage((prev) => Math.max(1, prev - 1))}
              onNext={() => setPage((prev) => prev + 1)}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default AttendancePage;
