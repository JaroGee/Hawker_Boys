"""initial schema"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "courses",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(length=64), nullable=False, unique=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "course_modules",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("course_id", pg.UUID(as_uuid=True), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("duration_hours", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("course_id", "code", name="uq_module_code_per_course"),
    )

    op.create_table(
        "class_runs",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("course_id", pg.UUID(as_uuid=True), sa.ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False, unique=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("ssg_run_id", sa.String(length=128), nullable=True, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "sessions",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("class_run_id", pg.UUID(as_uuid=True), sa.ForeignKey("class_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("module_id", pg.UUID(as_uuid=True), sa.ForeignKey("course_modules.id", ondelete="SET NULL"), nullable=True),
        sa.Column("session_date", sa.Date(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "trainers",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("contact_number", sa.String(length=32), nullable=True),
        sa.Column("ssg_trainer_id", sa.String(length=128), nullable=True, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "learners",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True, unique=True),
        sa.Column("contact_number", sa.String(length=32), nullable=True),
        sa.Column("hashed_identifier", sa.String(length=255), nullable=True, unique=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "enrollments",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("learner_id", pg.UUID(as_uuid=True), sa.ForeignKey("learners.id", ondelete="CASCADE"), nullable=False),
        sa.Column("class_run_id", pg.UUID(as_uuid=True), sa.ForeignKey("class_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.Enum("pending", "confirmed", "completed", "withdrawn", name="enrollmentstatus"), nullable=False, server_default="pending"),
        sa.Column("ssg_enrollment_id", sa.String(length=128), nullable=True, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("learner_id", "class_run_id", name="uq_enrollment_learner_run"),
    )

    op.create_table(
        "attendance",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("enrollment_id", pg.UUID(as_uuid=True), sa.ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("session_id", pg.UUID(as_uuid=True), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.Enum("present", "absent", "late", name="attendancestatus"), nullable=False),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("enrollment_id", "session_id", name="uq_attendance_unique"),
    )

    op.create_table(
        "assessments",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("enrollment_id", pg.UUID(as_uuid=True), sa.ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("passed", sa.Boolean(), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "certificates",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("assessment_id", pg.UUID(as_uuid=True), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("issued_on", sa.Date(), nullable=False),
        sa.Column("certificate_number", sa.String(length=128), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "session_trainers",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", pg.UUID(as_uuid=True), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("trainer_id", pg.UUID(as_uuid=True), sa.ForeignKey("trainers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("primary", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("session_id", "trainer_id", name="uq_session_trainer"),
    )

    op.create_table(
        "audit_trails",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column("actor_id", pg.UUID(as_uuid=True), nullable=True),
        sa.Column("actor_role", sa.String(length=64), nullable=True),
        sa.Column("entity_type", sa.String(length=128), nullable=False),
        sa.Column("entity_id", sa.String(length=128), nullable=False),
        sa.Column("action", sa.Enum("create", "update", "delete", "view", name="auditaction"), nullable=False),
        sa.Column("context", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("audit_trails")
    op.drop_table("session_trainers")
    op.drop_table("certificates")
    op.drop_table("assessments")
    op.drop_table("attendance")
    op.drop_table("enrollments")
    op.drop_table("learners")
    op.drop_table("trainers")
    op.drop_table("sessions")
    op.drop_table("class_runs")
    op.drop_table("course_modules")
    op.drop_table("courses")
    sa.Enum(name="auditaction").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="attendancestatus").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="enrollmentstatus").drop(op.get_bind(), checkfirst=False)
