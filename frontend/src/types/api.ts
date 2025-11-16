export type UUID = string;

export interface ModuleRead {
  id: UUID;
  title: string;
  description?: string | null;
  order: number;
}

export interface Course {
  id: UUID;
  code: string;
  title: string;
  description?: string | null;
  is_active: boolean;
  ssg_course_code?: string | null;
  created_at: string;
  updated_at: string;
  modules: ModuleRead[];
}

export interface CoursePayload {
  code: string;
  title: string;
  description?: string | null;
  modules?: { title: string; description?: string | null; order?: number }[];
}

export interface ClassRun {
  id: UUID;
  course_id: UUID;
  course_title: string;
  reference_code: string;
  start_date: string;
  end_date: string;
  status: string;
  ssg_run_id?: string | null;
  created_at: string;
  updated_at: string;
}

export interface Learner {
  id: UUID;
  given_name: string;
  family_name: string;
  date_of_birth?: string | null;
  contact_number?: string | null;
  masked_nric?: string | null;
  created_at: string;
  updated_at: string;
}

export interface Enrollment {
  id: UUID;
  learner_id: UUID;
  class_run_id: UUID;
  status: string;
  enrollment_date: string;
  ssg_enrollment_id?: string | null;
  created_at: string;
  updated_at: string;
}

export interface AttendanceRecord {
  id: UUID;
  enrollment_id: UUID;
  session_id: UUID;
  status: string;
  remarks?: string | null;
  submitted_to_ssg: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuditTrail {
  id: UUID;
  performed_by: UUID | null;
  action: string;
  entity_type: string;
  entity_id: string;
  timestamp: string;
  context?: string | null;
}

export interface UserProfile {
  id: UUID;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  last_login_at?: string | null;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export type PaginatedParams = {
  q?: string;
  page?: number;
  page_size?: number;
  sort?: string;
  [key: string]: string | number | undefined;
};

export interface LoginPayload {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  role: string;
}
