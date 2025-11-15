const Dashboard = () => {
  return (
    <section>
      <h2>Quick Actions</h2>
      <ol className="action-list">
        <li>Create a new course, then add class runs.</li>
        <li>Enroll learners into published class runs.</li>
        <li>Mark attendance after each session and submit assessments.</li>
        <li>Review SSG sync status and address any flagged issues.</li>
      </ol>
      <p className="hint">Need help? Refer to the operator runbook in docs/README.md.</p>
    </section>
  );
};

export default Dashboard;
