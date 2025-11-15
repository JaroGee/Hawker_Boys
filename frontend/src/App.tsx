import { useEffect, useState } from "react";
import axios from "axios";

type Course = {
  id: string;
  code: string;
  title: string;
};

function App() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios
      .get<Course[]>("/api/v1/courses", { headers: { "X-Role": "ops" } })
      .then((res) => setCourses(res.data))
      .catch(() =>
        setError("We could not load courses right now. Refresh the page or confirm the backend is running. Contact ops support if it keeps happening.")
      );
  }, []);

  return (
    <main style={{ margin: "2rem", fontFamily: "system-ui" }}>
      <h1>Hawker Boys TMS</h1>
      <p>Manage courses, class runs, and SSG sync from this lightweight console.</p>
      {error && <div style={{ color: "#c00", fontWeight: 600 }}>{error}</div>}
      <section>
        <h2>Courses</h2>
        {courses.length === 0 ? (
          <p>No courses yet. Create one via the API or seed script.</p>
        ) : (
          <ul>
            {courses.map((course) => (
              <li key={course.id}>
                <strong>{course.title}</strong> <span>({course.code})</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}

export default App;
