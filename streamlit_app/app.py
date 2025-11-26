from __future__ import annotations

import os
from datetime import date, datetime, timedelta
from typing import Any, Optional

import requests
import streamlit as st

DEFAULT_API_URL = os.getenv("TMS_API_URL", "http://localhost:8000/api")
CLASS_RUN_STATUSES = ["draft", "published", "completed", "cancelled"]
ENROLLMENT_STATUSES = ["registered", "in_progress", "completed", "withdrawn"]


st.set_page_config(page_title="Hawker Boys TMS (Streamlit)", page_icon="🔥", layout="wide")


def init_state() -> None:
    st.session_state.setdefault("api_url", DEFAULT_API_URL)
    st.session_state.setdefault("token", None)
    st.session_state.setdefault("profile", None)
    st.session_state.setdefault("nav", "Dashboard")
    st.session_state.setdefault("courses_page", 1)
    st.session_state.setdefault("runs_page", 1)
    st.session_state.setdefault("learners_page", 1)
    st.session_state.setdefault("enrollments_page", 1)
    st.session_state.setdefault("attendance_page", 1)


def clear_session() -> None:
    st.session_state["token"] = None
    st.session_state["profile"] = None


def api_request(method: str, path: str, **kwargs: Any) -> Optional[requests.Response]:
    base_url = (st.session_state.get("api_url") or DEFAULT_API_URL).rstrip("/")
    url = f"{base_url}{path if path.startswith('/') else '/' + path}"
    headers = kwargs.pop("headers", {})
    headers.setdefault("Accept", "application/json")

    token = st.session_state.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.request(method, url, headers=headers, timeout=15, **kwargs)
    except requests.RequestException as exc:
        st.error(f"Network error: {exc}")
        return None

    if response.status_code == 401:
        clear_session()
        st.warning("Session expired or invalid. Please sign in again.")
        return None

    if not response.ok:
        detail: Optional[str] = None
        try:
            detail = response.json().get("detail")
        except Exception:
            detail = response.text
        message = detail or "Request failed."
        st.error(f"{message} ({response.status_code})")
        return None

    return response


def api_json(method: str, path: str, **kwargs: Any) -> Optional[Any]:
    response = api_request(method, path, **kwargs)
    if response is None:
        return None
    try:
        return response.json()
    except ValueError:
        st.error("Could not decode server response.")
        return None


def format_date(value: str | None) -> str:
    if not value:
        return "—"
    try:
        return datetime.fromisoformat(value.replace("Z", "")).strftime("%Y-%m-%d")
    except ValueError:
        return value


def format_datetime(value: str | None) -> str:
    if not value:
        return "—"
    try:
        return datetime.fromisoformat(value.replace("Z", "")).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return value


def render_sidebar() -> str:
    st.sidebar.header("TMS Streamlit")
    st.sidebar.text_input(
        "API base URL",
        key="api_url",
        help="Include the /api prefix (e.g. http://localhost:8000/api).",
    )

    if st.session_state.get("profile"):
        profile = st.session_state["profile"]
        allowed_nav = ["Dashboard", "Courses & runs", "Learners", "Enrollments", "Attendance"]
        # If we previously stored a different nav (e.g. Login), reset to a safe default.
        if st.session_state.get("nav") not in allowed_nav:
            st.session_state["nav"] = allowed_nav[0]
        st.sidebar.success(f"{profile['full_name']} ({profile['role']})")
        nav = st.sidebar.radio(
            "Navigation",
            allowed_nav,
            key="nav",
        )
        if st.sidebar.button("Sign out"):
            clear_session()
            st.rerun()
        return nav

    st.sidebar.info("Sign in to access the TMS workspace.")
    st.session_state["nav"] = "Login"
    return "Login"


def render_login() -> None:
    st.title("Hawker Boys TMS (Streamlit)")
    st.caption("Sign in with your TMS credentials to continue.")

    with st.form("login-form"):
        email = st.text_input("Email", value="admin@hawkerboys.local")
        password = st.text_input("Password", type="password", value="ChangeMe123!")
        submitted = st.form_submit_button("Sign in")

    if submitted:
        data = api_json("post", "/auth/login", json={"email": email, "password": password})
        if data:
            st.session_state["token"] = data["access_token"]
            profile = api_json("get", "/auth/me")
            if profile:
                st.session_state["profile"] = profile
                st.success(f"Signed in as {profile['full_name']}")
                st.rerun()


def dashboard_page() -> None:
    st.title("Dashboard")
    st.caption("Pulse for courses, learners, and SSG syncs.")

    metrics = []
    for label, endpoint in [
        ("Courses", "/v1/courses"),
        ("Learners", "/v1/learners"),
        ("Enrollments", "/v1/enrollments"),
        ("Attendance records", "/v1/attendance"),
    ]:
        data = api_json("get", endpoint, params={"page_size": 1})
        metrics.append((label, data["total"] if data else None))

    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics):
        col.metric(label, "—" if value is None else f"{value:,}")

    st.subheader("Recent operator activity")
    audit = api_json("get", "/v1/audit", params={"page_size": 6})
    if audit and audit.get("items"):
        rows = [
            {
                "Action": event["action"],
                "Entity": f"{event['entity_type']} • {event['entity_id']}",
                "When": format_datetime(event["timestamp"]),
            }
            for event in audit["items"]
        ]
        st.table(rows)
    else:
        st.info("No audit events yet.")


def fetch_course_options(limit: int = 100) -> list[dict[str, str]]:
    data = api_json("get", "/v1/courses", params={"page_size": limit})
    if not data:
        return []
    return [{"id": item["id"], "label": f"{item['code']} — {item['title']}"} for item in data.get("items", [])]


def fetch_run_options(limit: int = 100) -> list[dict[str, str]]:
    data = api_json("get", "/v1/class-runs", params={"page_size": limit})
    if not data:
        return []
    return [
        {
            "id": item["id"],
            "label": f"{item['reference_code']} • {item['course_title']}",
        }
        for item in data.get("items", [])
    ]


def fetch_learner_options(limit: int = 100) -> list[dict[str, str]]:
    data = api_json("get", "/v1/learners", params={"page_size": limit})
    if not data:
        return []
    return [
        {
            "id": item["id"],
            "label": f"{item['given_name']} {item['family_name']} ({item.get('masked_nric') or 'no NRIC'})",
        }
        for item in data.get("items", [])
    ]


def courses_runs_page() -> None:
    st.title("Courses and runs")
    st.caption("Manage course shells and publish new class runs.")
    courses_tab, runs_tab = st.tabs(["Courses", "Class runs"])

    with courses_tab:
        search = st.text_input("Search by code or title", key="courses_search")
        page = st.session_state.get("courses_page", 1)
        data = api_json("get", "/v1/courses", params={"q": search or None, "page": page, "page_size": 10})

        st.write(f"Total courses: {data.get('total', 0) if data else 0}")
        if data and data.get("items"):
            rows = [
                {
                    "Code": course["code"],
                    "Title": course["title"],
                    "Status": "Active" if course["is_active"] else "Hidden",
                    "Updated": format_date(course["updated_at"]),
                }
                for course in data["items"]
            ]
            st.table(rows)
        else:
            st.info("No courses found. Add one below.")

        col_prev, col_next = st.columns(2)
        if col_prev.button("Previous page", disabled=page <= 1):
            st.session_state["courses_page"] = max(1, page - 1)
            st.rerun()
        if col_next.button("Next page"):
            st.session_state["courses_page"] = page + 1
            st.rerun()

        with st.expander("Create course"):
            with st.form("create-course-form"):
                code = st.text_input("Course code", help="Use the SSG-friendly reference.")
                title = st.text_input("Title")
                description = st.text_area("Description", "")
                modules_text = st.text_area(
                    "Modules (optional, one title per line)",
                    placeholder="Knife Skills\nMenu Planning\nCosting 101",
                )
                submit_course = st.form_submit_button("Create course")

            if submit_course:
                modules = []
                for idx, line in enumerate(modules_text.splitlines()):
                    title_line = line.strip()
                    if title_line:
                        modules.append({"title": title_line, "order": idx})

                payload = {
                    "code": code.strip(),
                    "title": title.strip(),
                    "description": description.strip() or None,
                    "modules": modules,
                }

                if not payload["code"] or not payload["title"]:
                    st.error("Course code and title are required.")
                else:
                    created = api_json("post", "/v1/courses", json=payload)
                    if created:
                        st.success(f"Created course {created.get('title')}")
                        st.session_state["courses_page"] = 1
                        st.rerun()

    with runs_tab:
        search = st.text_input("Filter by reference or course", key="runs_search")
        page = st.session_state.get("runs_page", 1)
        data = api_json("get", "/v1/class-runs", params={"q": search or None, "page": page, "page_size": 10})

        st.write(f"Total class runs: {data.get('total', 0) if data else 0}")
        if data and data.get("items"):
            rows = [
                {
                    "Reference": run["reference_code"],
                    "Course": run["course_title"],
                    "Status": run["status"],
                    "Schedule": f"{format_date(run['start_date'])} → {format_date(run['end_date'])}",
                }
                for run in data["items"]
            ]
            st.table(rows)
        else:
            st.info("No class runs found.")

        col_prev, col_next = st.columns(2)
        if col_prev.button("Previous", key="runs_prev", disabled=page <= 1):
            st.session_state["runs_page"] = max(1, page - 1)
            st.rerun()
        if col_next.button("Next", key="runs_next"):
            st.session_state["runs_page"] = page + 1
            st.rerun()

        with st.expander("Create class run"):
            course_options = fetch_course_options()
            if not course_options:
                st.info("Create a course first.")
            else:
                labels = [option["label"] for option in course_options]
                id_map = {option["label"]: option["id"] for option in course_options}

                with st.form("create-run-form"):
                    selected_label = st.selectbox("Course", labels)
                    reference_code = st.text_input("Reference code")
                    start_date = st.date_input("Start date", value=date.today())
                    end_date = st.date_input("End date", value=date.today() + timedelta(days=1))
                    status = st.selectbox("Status", CLASS_RUN_STATUSES, index=0)
                    submit_run = st.form_submit_button("Create class run")

                if submit_run:
                    course_id = id_map.get(selected_label)
                    if not reference_code.strip():
                        st.error("Reference code is required.")
                    elif end_date < start_date:
                        st.error("End date cannot be before the start date.")
                    else:
                        payload = {
                            "reference_code": reference_code.strip(),
                            "start_date": start_date.isoformat(),
                            "end_date": end_date.isoformat(),
                            "status": status,
                        }
                        created = api_json("post", f"/v1/courses/{course_id}/runs", json=payload)
                        if created:
                            st.success(f"Created run {created.get('reference_code')}")
                            st.session_state["runs_page"] = 1
                            st.rerun()


def learners_page() -> None:
    st.title("Learners")
    st.caption("Add learners and review their profiles.")

    search = st.text_input("Search by name or NRIC", key="learners_search")
    page = st.session_state.get("learners_page", 1)
    data = api_json("get", "/v1/learners", params={"q": search or None, "page": page, "page_size": 10})

    st.write(f"Total learners: {data.get('total', 0) if data else 0}")
    if data and data.get("items"):
        rows = [
            {
                "Name": f"{learner['given_name']} {learner['family_name']}",
                "Masked NRIC": learner.get("masked_nric") or "—",
                "Contact": learner.get("contact_number") or "—",
                "Created": format_date(learner["created_at"]),
            }
            for learner in data["items"]
        ]
        st.table(rows)
    else:
        st.info("No learners found.")

    col_prev, col_next = st.columns(2)
    if col_prev.button("Previous", key="learners_prev", disabled=page <= 1):
        st.session_state["learners_page"] = max(1, page - 1)
        st.rerun()
    if col_next.button("Next", key="learners_next"):
        st.session_state["learners_page"] = page + 1
        st.rerun()

    with st.expander("Create learner"):
        with st.form("create-learner-form"):
            given_name = st.text_input("Given name")
            family_name = st.text_input("Family name")
            include_dob = st.checkbox("Provide date of birth")
            dob_value = st.date_input("Date of birth", value=date.today()) if include_dob else None
            contact_number = st.text_input("Contact number (optional)")
            masked_nric = st.text_input("Masked NRIC (optional)", help="Use masked format, e.g. S1234567*.")
            submit_learner = st.form_submit_button("Create learner")

        if submit_learner:
            if not given_name.strip() or not family_name.strip():
                st.error("Given name and family name are required.")
            else:
                payload = {
                    "given_name": given_name.strip(),
                    "family_name": family_name.strip(),
                    "contact_number": contact_number.strip() or None,
                    "masked_nric": masked_nric.strip() or None,
                }
                if dob_value:
                    payload["date_of_birth"] = dob_value.isoformat()
                created = api_json("post", "/v1/learners", json=payload)
                if created:
                    st.success(f"Created learner {created.get('given_name')} {created.get('family_name')}")
                    st.session_state["learners_page"] = 1
                    st.rerun()


def enrollments_page() -> None:
    st.title("Enrollments")
    st.caption("Link learners to class runs.")

    search = st.text_input("Search by learner or class", key="enrollments_search")
    page = st.session_state.get("enrollments_page", 1)
    data = api_json("get", "/v1/enrollments", params={"q": search or None, "page": page, "page_size": 10})

    st.write(f"Total enrollments: {data.get('total', 0) if data else 0}")
    if data and data.get("items"):
        rows = [
            {
                "Enrollment ID": enrollment["id"][:8],
                "Learner": enrollment["learner_id"][:8],
                "Class run": enrollment["class_run_id"][:8],
                "Status": enrollment["status"].replace("_", " "),
                "Enrolled": format_date(enrollment["enrollment_date"]),
            }
            for enrollment in data["items"]
        ]
        st.table(rows)
    else:
        st.info("No enrollments found.")

    col_prev, col_next = st.columns(2)
    if col_prev.button("Previous", key="enrollments_prev", disabled=page <= 1):
        st.session_state["enrollments_page"] = max(1, page - 1)
        st.rerun()
    if col_next.button("Next", key="enrollments_next"):
        st.session_state["enrollments_page"] = page + 1
        st.rerun()

    with st.expander("Create enrollment"):
        learner_options = fetch_learner_options()
        run_options = fetch_run_options()
        if not learner_options or not run_options:
            st.info("Create at least one learner and class run to enroll.")
        else:
            learner_labels = [option["label"] for option in learner_options]
            learner_map = {option["label"]: option["id"] for option in learner_options}

            run_labels = [option["label"] for option in run_options]
            run_map = {option["label"]: option["id"] for option in run_options}

            with st.form("create-enrollment-form"):
                learner_label = st.selectbox("Learner", learner_labels)
                run_label = st.selectbox("Class run", run_labels)
                status = st.selectbox("Status", ENROLLMENT_STATUSES, index=0)
                submit_enrollment = st.form_submit_button("Enroll learner")

            if submit_enrollment:
                payload = {
                    "learner_id": learner_map.get(learner_label),
                    "class_run_id": run_map.get(run_label),
                    "status": status,
                }
                created = api_json("post", "/v1/enrollments", json=payload)
                if created:
                    st.success("Enrollment created.")
                    st.session_state["enrollments_page"] = 1
                    st.rerun()


def attendance_page() -> None:
    st.title("Attendance")
    st.caption("Session-level acknowledgement.")

    search = st.text_input("Search by enrollment or session", key="attendance_search")
    page = st.session_state.get("attendance_page", 1)
    data = api_json("get", "/v1/attendance", params={"q": search or None, "page": page, "page_size": 10})

    st.write(f"Total attendance records: {data.get('total', 0) if data else 0}")
    if data and data.get("items"):
        rows = [
            {
                "Enrollment": record["enrollment_id"][:8],
                "Session": record["session_id"][:8],
                "Status": record["status"],
                "Submitted": "Synced" if record["submitted_to_ssg"] else "Pending",
                "Updated": format_datetime(record["updated_at"]),
            }
            for record in data["items"]
        ]
        st.table(rows)
    else:
        st.info("No attendance records.")

    col_prev, col_next = st.columns(2)
    if col_prev.button("Previous", key="attendance_prev", disabled=page <= 1):
        st.session_state["attendance_page"] = max(1, page - 1)
        st.rerun()
    if col_next.button("Next", key="attendance_next"):
        st.session_state["attendance_page"] = page + 1
        st.rerun()


def main() -> None:
    init_state()
    nav_choice = render_sidebar()

    if not st.session_state.get("token"):
        render_login()
        return

    if nav_choice == "Dashboard":
        dashboard_page()
    elif nav_choice == "Courses & runs":
        courses_runs_page()
    elif nav_choice == "Learners":
        learners_page()
    elif nav_choice == "Enrollments":
        enrollments_page()
    elif nav_choice == "Attendance":
        attendance_page()
    else:
        dashboard_page()


if __name__ == "__main__":
    main()
