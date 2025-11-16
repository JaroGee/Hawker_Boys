import { FormEvent, useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { Drawer } from '../components/Drawer';
import { EmptyState } from '../components/EmptyState';
import { ErrorState } from '../components/ErrorState';
import { FormField } from '../components/FormField';
import { LoadingState } from '../components/LoadingState';
import { PaginationControls } from '../components/PaginationControls';
import { StatusBadge } from '../components/StatusBadge';
import { useToast } from '../context/ToastContext';
import { useDebounce } from '../hooks/useDebounce';
import { createCourse, deleteCourse, fetchCourses, updateCourse } from '../lib/api';
import type { Course, CoursePayload } from '../types/api';

type DrawerState =
  | { mode: 'closed' }
  | { mode: 'create' }
  | { mode: 'view'; course: Course }
  | { mode: 'edit'; course: Course };

const emptyPayload: CoursePayload = {
  code: '',
  title: '',
  description: '',
  modules: [],
};

const CourseForm = ({
  initialValues,
  onSubmit,
  submitting,
}: {
  initialValues: CoursePayload;
  onSubmit: (payload: CoursePayload) => Promise<void>;
  submitting: boolean;
}) => {
  const [form, setForm] = useState<CoursePayload>(initialValues);
  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!form.code.trim() || !form.title.trim()) return;
    await onSubmit({
      ...form,
      modules: form.modules ?? [],
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormField label="Course code" htmlFor="course-code" hint="Use the SSG-friendly reference.">
        <input
          id="course-code"
          value={form.code}
          onChange={(event) => setForm((prev) => ({ ...prev, code: event.target.value }))}
          required
        />
      </FormField>
      <FormField label="Title" htmlFor="course-title">
        <input
          id="course-title"
          value={form.title}
          onChange={(event) => setForm((prev) => ({ ...prev, title: event.target.value }))}
          required
        />
      </FormField>
      <FormField label="Description" htmlFor="course-description">
        <textarea
          id="course-description"
          value={form.description ?? ''}
          onChange={(event) => setForm((prev) => ({ ...prev, description: event.target.value }))}
        />
      </FormField>
      <button type="submit" className="hb-button hb-button--primary" disabled={submitting}>
        {submitting ? 'Saving…' : 'Save'}
      </button>
    </form>
  );
};

const CoursesPage = () => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 300);
  const [drawer, setDrawer] = useState<DrawerState>({ mode: 'closed' });
  const toast = useToast();
  const queryClient = useQueryClient();

  const coursesQuery = useQuery({
    queryKey: ['courses', debouncedSearch, page],
    queryFn: async () => {
      const response = await fetchCourses({ q: debouncedSearch, page, page_size: 10 });
      return response.data;
    },
    keepPreviousData: true,
  });

  const createMutation = useMutation({
    mutationFn: (payload: CoursePayload) => createCourse(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['courses'] });
      toast.push({ title: 'Course created', tone: 'success' });
      setDrawer({ mode: 'closed' });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<CoursePayload> }) => updateCourse(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['courses'] });
      toast.push({ title: 'Course updated', tone: 'success' });
      setDrawer({ mode: 'closed' });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteCourse(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['courses'] });
      toast.push({ title: 'Course removed', tone: 'success' });
    },
  });

  const handleDelete = (course: Course) => {
    if (window.confirm(`Delete ${course.title}? This removes all runs under it.`)) {
      deleteMutation.mutate(course.id);
    }
  };

  const rows = coursesQuery.data?.items ?? [];

  const drawerContent = useMemo(() => {
    if (drawer.mode === 'closed') return null;
    if (drawer.mode === 'view') {
      const { course } = drawer;
      return (
        <Drawer
          title={course.title}
          description={course.code}
          isOpen
          onClose={() => setDrawer({ mode: 'closed' })}
        >
          <p>{course.description || 'No description provided.'}</p>
          <p className="page-subtitle">
            Created {new Date(course.created_at).toLocaleDateString()} •{' '}
            {course.modules.length} modules
          </p>
        </Drawer>
      );
    }
    if (drawer.mode === 'create') {
      return (
        <Drawer
          title="New course"
          description="Define the shell before adding runs."
          isOpen
          onClose={() => setDrawer({ mode: 'closed' })}
        >
          <CourseForm initialValues={emptyPayload} onSubmit={(payload) => createMutation.mutateAsync(payload)} submitting={createMutation.isPending} />
        </Drawer>
      );
    }
    if (drawer.mode === 'edit') {
      const { course } = drawer;
      return (
        <Drawer
          title={`Edit ${course.title}`}
          description={course.code}
          isOpen
          onClose={() => setDrawer({ mode: 'closed' })}
        >
          <CourseForm
            initialValues={{
              code: course.code,
              title: course.title,
              description: course.description,
            }}
            onSubmit={(payload) => updateMutation.mutateAsync({ id: course.id, payload })}
            submitting={updateMutation.isPending}
          />
        </Drawer>
      );
    }
    return null;
  }, [drawer, createMutation.isPending, updateMutation.isPending]);

  if (coursesQuery.isLoading) return <LoadingState label="Loading courses" />;
  if (coursesQuery.isError)
    return (
      <ErrorState
        message="Unable to load courses."
        action={
          <button type="button" className="hb-button hb-button--primary" onClick={() => coursesQuery.refetch()}>
            Retry
          </button>
        }
      />
    );

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Courses</h1>
          <p className="page-subtitle">Publish-ready programmes that sync with SSG.</p>
        </div>
        <button type="button" className="hb-button hb-button--primary" onClick={() => setDrawer({ mode: 'create' })}>
          New course
        </button>
      </div>
      <div className="card" style={{ marginBottom: 'var(--hb-space-lg)' }}>
        <input
          className="search-input"
          placeholder="Search by code or title"
          value={search}
          onChange={(event) => {
            setSearch(event.target.value);
            setPage(1);
          }}
        />
      </div>
      <div className="card">
        {rows.length === 0 ? (
          <EmptyState
            title="No courses yet"
            description="Create your first course to unlock class runs and enrollments."
            action={
              <button type="button" className="hb-button hb-button--primary" onClick={() => setDrawer({ mode: 'create' })}>
                Create course
              </button>
            }
          />
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Title</th>
                  <th>Status</th>
                  <th>Updated</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((course) => (
                  <tr key={course.id}>
                    <td>{course.code}</td>
                    <td>{course.title}</td>
                    <td>
                      <StatusBadge label={course.is_active ? 'Active' : 'Hidden'} tone={course.is_active ? 'success' : 'danger'} />
                    </td>
                    <td>{new Date(course.updated_at).toLocaleDateString()}</td>
                    <td>
                      <div className="table-actions">
                        <button type="button" className="hb-button hb-button--ghost" onClick={() => setDrawer({ mode: 'view', course })}>
                          View
                        </button>
                        <button type="button" className="hb-button hb-button--secondary" onClick={() => setDrawer({ mode: 'edit', course })}>
                          Edit
                        </button>
                        <button type="button" className="hb-button hb-button--ghost" onClick={() => handleDelete(course)}>
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <PaginationControls
              page={page}
              pageSize={10}
              total={coursesQuery.data?.total ?? 0}
              onPrevious={() => setPage((prev) => Math.max(1, prev - 1))}
              onNext={() => setPage((prev) => prev + 1)}
            />
          </>
        )}
      </div>
      {drawerContent}
    </div>
  );
};

export default CoursesPage;
