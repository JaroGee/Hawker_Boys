from __future__ import annotations

from tms.domain.models import Course
from tms.infra.database import SessionLocal


def run() -> None:
    with SessionLocal() as session:
        if session.query(Course).count() == 0:
            demo = Course(code="FINLIT-101", title="Financial Literacy Essentials", description="Basics of budgeting for returning citizens.")
            session.add(demo)
            session.commit()
            print("Seeded demo course.")
        else:
            print("Seed skipped: records already exist.")


if __name__ == "__main__":
    run()
