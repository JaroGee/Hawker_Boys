import { useQuery } from '@tanstack/react-query';

import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { fetchAttendance, fetchAudit, fetchCourses, fetchEnrollments, fetchLearners } from '../lib/api';
import type { AuditTrail } from '../types/api';

const useDashboardData = () =>
  useQuery({
    queryKey: ['dashboard'],
    queryFn: async () => {
      const [courses, learners, enrollments, attendance, audit] = await Promise.all([
        fetchCourses({ page_size: 1 }),
        fetchLearners({ page_size: 1 }),
        fetchEnrollments({ page_size: 1 }),
        fetchAttendance({ page_size: 1 }),
        fetchAudit({ page_size: 6 }),
      ]);

      return {
        metrics: [
          { label: 'Courses', value: courses.data.total },
          { label: 'Learners', value: learners.data.total },
          { label: 'Enrollments', value: enrollments.data.total },
          { label: 'Attendance records', value: attendance.data.total },
        ],
        activity: audit.data.items,
      };
    },
  });

const DashboardPage = () => {
  const { data, isLoading, isError, refetch } = useDashboardData();

  if (isLoading) return <LoadingState label="Loading dashboard" />;
  if (isError || !data)
    return (
      <ErrorState
        message="We could not load the KPIs. Please refresh to try again."
        action={
          <button type="button" className="hb-button hb-button--primary" onClick={() => refetch()}>
            Retry
          </button>
        }
      />
    );

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Pulse for the academy and SSG queue.</p>
        </div>
      </div>
      <div className="kpi-grid">
        {data.metrics.map((metric) => (
          <div className="card kpi-tile" key={metric.label}>
            <span className="kpi-tile__label">{metric.label}</span>
            <span className="kpi-tile__value">{metric.value.toLocaleString()}</span>
          </div>
        ))}
      </div>

      <div className="card">
        <h2>Recent Operator Activity</h2>
        {data.activity.length === 0 ? (
          <p className="page-subtitle">No activity logged across the last 24 hours.</p>
        ) : (
          <ul className="activity-list">
            {data.activity.map((event: AuditTrail) => (
              <li key={event.id} className="activity-item">
                <div>
                  <strong>{event.action.toUpperCase()}</strong>
                  <p className="page-subtitle">
                    {event.entity_type} • {event.entity_id}
                  </p>
                </div>
                <span className="activity-meta">
                  {new Date(event.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
