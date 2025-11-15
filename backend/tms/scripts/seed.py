from __future__ import annotations

import datetime as dt

from tms.auth.security import hash_password
from tms.domain import models
from tms.infra.database import session_scope


def main() -> None:
    with session_scope() as session:
        if session.query(models.Course).first():
            print("Seed data already present")
            return

        admin = models.User(
            email="seed-admin@hawkerboys.sg",
            full_name="Seed Admin",
            password_hash=hash_password("ChangeMe123!"),
            role=models.UserRoleEnum.ADMIN,
        )
        session.add(admin)

        course = models.Course(code="FIN-LIT-101", title="Financial Literacy Basics", description="Budgeting and savings skills")
        session.add(course)

        class_run = models.ClassRun(
            course=course,
            reference_code="FIN-2024-01",
            start_date=dt.date.today(),
            end_date=dt.date.today() + dt.timedelta(days=30),
            status=models.ClassRunStatusEnum.PUBLISHED,
        )
        session.add(class_run)

        learner = models.Learner(given_name="Alex", family_name="Tan", masked_nric="S1234567*")
        session.add(learner)

        enrollment = models.Enrollment(
            learner=learner,
            class_run=class_run,
            status=models.EnrollmentStatusEnum.REGISTERED,
        )
        session.add(enrollment)

        session.commit()
        print("Seed data created")


if __name__ == "__main__":
    main()
