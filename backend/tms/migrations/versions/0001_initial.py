"""Initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2024-06-06
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "courses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("ssg_course_code", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_courses_ssg_course_code", "courses", ["ssg_course_code"])

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("admin", "trainer", "ops", "learner", name="userroleenum"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "modules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_modules_course_id_order", "modules", ["course_id", "order"])

    op.create_table(
        "class_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reference_code", sa.String(length=100), nullable=False, unique=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("draft", "published", "completed", "cancelled", name="classrunstatusenum"),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("ssg_run_id", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_class_runs_course_status", "class_runs", ["course_id", "status"])
    op.create_index("ix_class_runs_ssg_run_id", "class_runs", ["ssg_run_id"])

    op.create_table(
        "sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("class_run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("class_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("session_date", sa.Date(), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_unique_constraint("uq_session_date_per_run", "sessions", ["class_run_id", "session_date"])

    op.create_table(
        "learners",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("given_name", sa.String(length=255), nullable=False),
        sa.Column("family_name", sa.String(length=255), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("contact_number", sa.String(length=50), nullable=True),
        sa.Column("masked_nric", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_learners_masked_nric", "learners", ["masked_nric"])

    op.create_table(
        "trainers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("certifications", sa.Text(), nullable=True),
        sa.Column("ssg_trainer_id", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_trainers_ssg_trainer_id", "trainers", ["ssg_trainer_id"])

    op.create_table(
        "enrollments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("learner_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("learners.id", ondelete="CASCADE"), nullable=False),
        sa.Column("class_run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("class_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "status",
            sa.Enum("registered", "in_progress", "completed", "withdrawn", name="enrollmentstatusenum"),
            nullable=False,
        ),
        sa.Column("enrollment_date", sa.Date(), nullable=False),
        sa.Column("ssg_enrollment_id", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_unique_constraint("uq_enrollment_per_class_run", "enrollments", ["learner_id", "class_run_id"])
    op.create_index("ix_enrollments_ssg_enrollment_id", "enrollments", ["ssg_enrollment_id"])

    op.create_table(
        "trainer_sessions",
        sa.Column("trainer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("trainers.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "attendance",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("enrollment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.Enum("present", "absent", "late", name="attendancestatusenum"), nullable=False),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("submitted_to_ssg", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_unique_constraint(
        "uq_attendance_enrollment_session", "attendance", ["enrollment_id", "session_id"]
    )

    op.create_table(
        "assessments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("enrollment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("assessed_on", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "certificates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("enrollment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("enrollments.id", ondelete="CASCADE"), unique=True),
        sa.Column("issued_on", sa.Date(), nullable=False),
        sa.Column("certificate_url", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "audit_trails",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("performed_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "action",
            sa.Enum("create", "update", "delete", "export", "access", name="auditactionenum"),
            nullable=False,
        ),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.String(length=100), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("context", sa.Text(), nullable=True),
    )
    op.create_index("ix_audit_entity", "audit_trails", ["entity_type", "entity_id"])


    op.create_index("ix_class_runs_reference_code", "class_runs", ["reference_code"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_class_runs_reference_code", table_name="class_runs")
    op.drop_index("ix_audit_entity", table_name="audit_trails")
    op.drop_table("audit_trails")
    op.drop_table("certificates")
    op.drop_table("assessments")
    op.drop_constraint("uq_attendance_enrollment_session", "attendance", type_="unique")
    op.drop_table("attendance")
    op.drop_table("trainer_sessions")
    op.drop_index("ix_enrollments_ssg_enrollment_id", table_name="enrollments")
    op.drop_constraint("uq_enrollment_per_class_run", "enrollments", type_="unique")
    op.drop_table("enrollments")
    op.drop_index("ix_trainers_ssg_trainer_id", table_name="trainers")
    op.drop_table("trainers")
    op.drop_index("ix_learners_masked_nric", table_name="learners")
    op.drop_table("learners")
    op.drop_constraint("uq_session_date_per_run", "sessions", type_="unique")
    op.drop_table("sessions")
    op.drop_index("ix_class_runs_ssg_run_id", table_name="class_runs")
    op.drop_index("ix_class_runs_course_status", table_name="class_runs")
    op.drop_table("class_runs")
    op.drop_index("ix_modules_course_id_order", table_name="modules")
    op.drop_table("modules")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_courses_ssg_course_code", table_name="courses")
    op.drop_table("courses")
