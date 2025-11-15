from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tms.infra.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text())
    is_published: Mapped[bool] = mapped_column(Boolean(), default=False)

    modules: Mapped[list[CourseModule]] = relationship("CourseModule", back_populates="course", cascade="all, delete-orphan")
    runs: Mapped[list[ClassRun]] = relationship("ClassRun", back_populates="course")


class CourseModule(Base, TimestampMixin):
    __tablename__ = "course_modules"
    __table_args__ = (UniqueConstraint("course_id", "code", name="uq_module_code_per_course"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text())
    duration_hours: Mapped[int] = mapped_column()

    course: Mapped[Course] = relationship("Course", back_populates="modules")


class ClassRun(Base, TimestampMixin):
    __tablename__ = "class_runs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="RESTRICT"), index=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    start_date: Mapped[date] = mapped_column(Date())
    end_date: Mapped[date] = mapped_column(Date())
    capacity: Mapped[int] = mapped_column()
    location: Mapped[str | None] = mapped_column(String(255))
    ssg_run_id: Mapped[str | None] = mapped_column(String(128), index=True, unique=True)

    course: Mapped[Course] = relationship("Course", back_populates="runs")
    sessions: Mapped[list[Session]] = relationship("Session", back_populates="class_run", cascade="all, delete-orphan")
    enrollments: Mapped[list[Enrollment]] = relationship("Enrollment", back_populates="class_run")


class Session(Base, TimestampMixin):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    class_run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("class_runs.id", ondelete="CASCADE"), index=True)
    module_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("course_modules.id", ondelete="SET NULL"), nullable=True)
    session_date: Mapped[date] = mapped_column(Date())
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    class_run: Mapped[ClassRun] = relationship("ClassRun", back_populates="sessions")
    module: Mapped[CourseModule | None] = relationship("CourseModule")
    attendance_records: Mapped[list[Attendance]] = relationship("Attendance", back_populates="session", cascade="all, delete-orphan")


class Trainer(Base, TimestampMixin):
    __tablename__ = "trainers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    contact_number: Mapped[str | None] = mapped_column(String(32))
    ssg_trainer_id: Mapped[str | None] = mapped_column(String(128), index=True, unique=True)

    sessions: Mapped[list[SessionTrainer]] = relationship("SessionTrainer", back_populates="trainer")


class Learner(Base, TimestampMixin):
    __tablename__ = "learners"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    contact_number: Mapped[str | None] = mapped_column(String(32))
    hashed_identifier: Mapped[str | None] = mapped_column(String(255), unique=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date(), nullable=True)

    enrollments: Mapped[list[Enrollment]] = relationship("Enrollment", back_populates="learner")


class EnrollmentStatus(PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    WITHDRAWN = "withdrawn"


class Enrollment(Base, TimestampMixin):
    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("learner_id", "class_run_id", name="uq_enrollment_learner_run"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    learner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("learners.id", ondelete="CASCADE"), index=True)
    class_run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("class_runs.id", ondelete="CASCADE"), index=True)
    status: Mapped[EnrollmentStatus] = mapped_column(Enum(EnrollmentStatus), default=EnrollmentStatus.PENDING)
    ssg_enrollment_id: Mapped[str | None] = mapped_column(String(128), index=True, unique=True)

    learner: Mapped[Learner] = relationship("Learner", back_populates="enrollments")
    class_run: Mapped[ClassRun] = relationship("ClassRun", back_populates="enrollments")
    attendance_records: Mapped[list[Attendance]] = relationship("Attendance", back_populates="enrollment")
    assessments: Mapped[list[Assessment]] = relationship("Assessment", back_populates="enrollment")


class AttendanceStatus(PyEnum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"


class Attendance(Base, TimestampMixin):
    __tablename__ = "attendance"
    __table_args__ = (UniqueConstraint("enrollment_id", "session_id", name="uq_attendance_unique"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    enrollment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("enrollments.id", ondelete="CASCADE"), index=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"), index=True)
    status: Mapped[AttendanceStatus] = mapped_column(Enum(AttendanceStatus))
    remarks: Mapped[str | None] = mapped_column(Text())

    enrollment: Mapped[Enrollment] = relationship("Enrollment", back_populates="attendance_records")
    session: Mapped[Session] = relationship("Session", back_populates="attendance_records")


class Assessment(Base, TimestampMixin):
    __tablename__ = "assessments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    enrollment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("enrollments.id", ondelete="CASCADE"), index=True)
    score: Mapped[float | None] = mapped_column()
    passed: Mapped[bool | None] = mapped_column(Boolean())
    remarks: Mapped[str | None] = mapped_column(Text())

    enrollment: Mapped[Enrollment] = relationship("Enrollment", back_populates="assessments")
    certificate: Mapped[Certificate | None] = relationship("Certificate", back_populates="assessment", uselist=False)


class Certificate(Base, TimestampMixin):
    __tablename__ = "certificates"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    assessment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessments.id", ondelete="CASCADE"), unique=True)
    issued_on: Mapped[date] = mapped_column(Date())
    certificate_number: Mapped[str] = mapped_column(String(128), unique=True)

    assessment: Mapped[Assessment] = relationship("Assessment", back_populates="certificate")


class SessionTrainer(Base, TimestampMixin):
    __tablename__ = "session_trainers"
    __table_args__ = (UniqueConstraint("session_id", "trainer_id", name="uq_session_trainer"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"), index=True)
    trainer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("trainers.id", ondelete="CASCADE"), index=True)
    primary: Mapped[bool] = mapped_column(Boolean(), default=True)

    session: Mapped[Session] = relationship("Session")
    trainer: Mapped[Trainer] = relationship("Trainer", back_populates="sessions")


class AuditAction(PyEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    VIEW = "view"


class AuditTrail(Base, TimestampMixin):
    __tablename__ = "audit_trails"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True, index=True)
    actor_role: Mapped[str | None] = mapped_column(String(64))
    entity_type: Mapped[str] = mapped_column(String(128), index=True)
    entity_id: Mapped[str] = mapped_column(String(128))
    action: Mapped[AuditAction] = mapped_column(Enum(AuditAction))
    context: Mapped[str | None] = mapped_column(Text())

