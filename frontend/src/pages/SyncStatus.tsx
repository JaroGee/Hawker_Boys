const SyncStatus = () => {
  return (
    <section>
      <h2>SSG Sync Status</h2>
      <p>Check the background job queue and logs for recent SSG sync attempts.</p>
      <ul className="status-help">
        <li>Green - Successfully synced.</li>
        <li>Amber - Pending retry, review logs.</li>
        <li>Red - Requires operator follow-up. See docs/SSG-Error-Catalog.md.</li>
      </ul>
    </section>
  );
};

export default SyncStatus;
