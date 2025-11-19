from __future__ import annotations

import datetime as dt
import uuid

from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tms.infra.database import Base


def _enum_values(enum_cls: type[PyEnum]) -> list[str]:
    return [member.value for member in enum_cls]


def str_enum(enum_cls: type[PyEnum]) -> SQLEnum:
    return SQLEnum(enum_cls, name=enum_cls.__name__.lower(), values_callable=_enum_values)


class TimestampMixin:
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), default=dt.datetime.utcnow, nullable=False
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow
    )


class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    ssg_course_code: Mapped[str | None] = mapped_column(String(100), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    modules: Mapped[list["Module"]] = relationship(back_populates="course", cascade="all, delete-orphan")
    runs: Mapped[list["ClassRun"]] = relationship(back_populates="course", cascade="all, delete-orphan")


class Module(Base, TimestampMixin):
    __tablename__ = "modules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, default=0)

    course: Mapped[Course] = relationship(back_populates="modules")

    __table_args__ = (Index("ix_modules_course_id_order", "course_id", "order"),)


class ClassRunStatusEnum(str, PyEnum):  # type: ignore[misc]
    DRAFT = "draft"
    PUBLISHED = "published"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ClassRun(Base, TimestampMixin):
    __tablename__ = "class_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    reference_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    start_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    status: Mapped[ClassRunStatusEnum] = mapped_column(
        str_enum(ClassRunStatusEnum), default=ClassRunStatusEnum.DRAFT
    )
    ssg_run_id: Mapped[str | None] = mapped_column(String(100), index=True)

    course: Mapped[Course] = relationship(back_populates="runs")
    sessions: Mapped[list["Session"]] = relationship(back_populates="class_run", cascade="all, delete-orphan")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="class_run", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_class_runs_course_status", "course_id", "status"),
    )

    @property
    def course_title(self) -> str:
        return self.course.title if self.course else ""


class Session(Base, TimestampMixin):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    class_run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("class_runs.id", ondelete="CASCADE"), nullable=False)
    session_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    location: Mapped[str | None] = mapped_column(String(255))
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    class_run: Mapped[ClassRun] = relationship(back_populates="sessions")
    attendance_records: Mapped[list["Attendance"]] = relationship(back_populates="session", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("class_run_id", "session_date", name="uq_session_date_per_run"),
    )


class UserRoleEnum(str, PyEnum):  # type: ignore[misc]
    ADMIN = "admin"
    TRAINER = "trainer"
    OPS = "ops"
    LEARNER = "learner"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRoleEnum] = mapped_column(str_enum(UserRoleEnum), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True))


class Learner(Base, TimestampMixin):
    __tablename__ = "learners"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    given_name: Mapped[str] = mapped_column(String(255), nullable=False)
    family_name: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[dt.date | None] = mapped_column(Date)
    contact_number: Mapped[str | None] = mapped_column(String(50))
    masked_nric: Mapped[str | None] = mapped_column(String(20), index=True)

    user: Mapped[User | None] = relationship()
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="learner")


class Trainer(Base, TimestampMixin):
    __tablename__ = "trainers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    bio: Mapped[str | None] = mapped_column(Text)
    certifications: Mapped[str | None] = mapped_column(Text)
    ssg_trainer_id: Mapped[str | None] = mapped_column(String(100), index=True)

    user: Mapped[User | None] = relationship()
    sessions: Mapped[list[Session]] = relationship(secondary="trainer_sessions", back_populates="trainers")


class TrainerSession(Base):
    __tablename__ = "trainer_sessions"

    trainer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("trainers.id", ondelete="CASCADE"), primary_key=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True)


Session.trainers = relationship(  # type: ignore[attr-defined]
    "Trainer", secondary="trainer_sessions", back_populates="sessions"
)


class EnrollmentStatusEnum(str, PyEnum):  # type: ignore[misc]
    REGISTERED = "registered"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    WITHDRAWN = "withdrawn"


class Enrollment(Base, TimestampMixin):
    __tablename__ = "enrollments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    learner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("learners.id", ondelete="CASCADE"), nullable=False)
    class_run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("class_runs.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[EnrollmentStatusEnum] = mapped_column(str_enum(EnrollmentStatusEnum), nullable=False)
    enrollment_date: Mapped[dt.date] = mapped_column(Date, default=dt.date.today)
    ssg_enrollment_id: Mapped[str | None] = mapped_column(String(100), index=True)

    learner: Mapped[Learner] = relationship(back_populates="enrollments")
    class_run: Mapped[ClassRun] = relationship(back_populates="enrollments")
    attendance_records: Mapped[list["Attendance"]] = relationship(back_populates="enrollment")

    __table_args__ = (
        UniqueConstraint("learner_id", "class_run_id", name="uq_enrollment_per_class_run"),
    )


class AttendanceStatusEnum(str, PyEnum):  # type: ignore[misc]
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"


class Attendance(Base, TimestampMixin):
    __tablename__ = "attendance"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrollment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[AttendanceStatusEnum] = mapped_column(str_enum(AttendanceStatusEnum), nullable=False)
    remarks: Mapped[str | None] = mapped_column(Text)
    submitted_to_ssg: Mapped[bool] = mapped_column(Boolean, default=False)

    enrollment: Mapped[Enrollment] = relationship(back_populates="attendance_records")
    session: Mapped[Session] = relationship(back_populates="attendance_records")

    __table_args__ = (
        UniqueConstraint("enrollment_id", "session_id", name="uq_attendance_enrollment_session"),
    )


class Assessment(Base, TimestampMixin):
    __tablename__ = "assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrollment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    remarks: Mapped[str | None] = mapped_column(Text)
    assessed_on: Mapped[dt.date] = mapped_column(Date, default=dt.date.today)

    enrollment: Mapped[Enrollment] = relationship()


class Certificate(Base, TimestampMixin):
    __tablename__ = "certificates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrollment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("enrollments.id", ondelete="CASCADE"), unique=True)
    issued_on: Mapped[dt.date] = mapped_column(Date, default=dt.date.today)
    certificate_url: Mapped[str] = mapped_column(String(255), nullable=False)

    enrollment: Mapped[Enrollment] = relationship()


class AuditActionEnum(str, PyEnum):  # type: ignore[misc]
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    ACCESS = "access"


class AuditTrail(Base):
    __tablename__ = "audit_trails"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    performed_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), index=True)
    action: Mapped[AuditActionEnum] = mapped_column(str_enum(AuditActionEnum), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False)
    timestamp: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=dt.datetime.utcnow)
    context: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        Index("ix_audit_entity", "entity_type", "entity_id"),
    )
