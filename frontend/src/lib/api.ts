import axios, { AxiosError } from 'axios';

import { authStorage } from './authStorage';
import type {
  AttendanceRecord,
  AuditTrail,
  ClassRun,
  Course,
  CoursePayload,
  Enrollment,
  Learner,
  LoginPayload,
  PaginatedParams,
  PaginatedResponse,
  TokenResponse,
  UserProfile,
} from '../types/api';

const baseURL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL,
  timeout: 15000,
});

apiClient.interceptors.request.use((config) => {
  const token = authStorage.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  config.headers.Accept = 'application/json';
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      authStorage.clear();
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  },
);

const withParams = (params: PaginatedParams = {}) => ({
  params: {
    page_size: 10,
    page: 1,
    sort: '-created_at',
    ...params,
  },
});

export const loginRequest = (payload: LoginPayload) => apiClient.post<TokenResponse>('/auth/login', payload);
export const meRequest = () => apiClient.get<UserProfile>('/auth/me');

export const fetchCourses = (params?: PaginatedParams) =>
  apiClient.get<PaginatedResponse<Course>>('/v1/courses', withParams(params));

export const fetchCourse = (id: string) => apiClient.get<Course>(`/v1/courses/${id}`);
export const createCourse = (payload: CoursePayload) => apiClient.post<Course>('/v1/courses', payload);
export const updateCourse = (id: string, payload: Partial<CoursePayload>) =>
  apiClient.patch<Course>(`/v1/courses/${id}`, payload);
export const deleteCourse = (id: string) => apiClient.delete<void>(`/v1/courses/${id}`);

export const fetchClassRuns = (params?: PaginatedParams) =>
  apiClient.get<PaginatedResponse<ClassRun>>('/v1/class-runs', withParams(params));

export const fetchLearners = (params?: PaginatedParams) =>
  apiClient.get<PaginatedResponse<Learner>>('/v1/learners', withParams(params));

export const fetchEnrollments = (params?: PaginatedParams) =>
  apiClient.get<PaginatedResponse<Enrollment>>('/v1/enrollments', withParams(params));

export const fetchAttendance = (params?: PaginatedParams) =>
  apiClient.get<PaginatedResponse<AttendanceRecord>>('/v1/attendance', withParams(params));

export const fetchAudit = (params?: PaginatedParams) =>
  apiClient.get<PaginatedResponse<AuditTrail>>('/v1/audit', withParams(params));

export const triggerWebhookTest = (secret: string) =>
  apiClient.post('/ssg/test-webhook', undefined, { headers: { 'X-SSG-Webhook-Secret': secret } });
