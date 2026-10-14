import { NavLink, Link, Outlet } from "react-router-dom";
import { FileSearch } from "lucide-react";

function DashboardLayout() {
  return (
    <div className="dashboard-layout">
      <aside className="dashboard-sidebar">
        <Link to="/" className="dashboard-brand">
          <FileSearch size={24} />
          <span>ResumeAI</span>
        </Link>

        <nav className="dashboard-navigation">
          <NavLink to="/dashboard" end>
            Overview
          </NavLink>

          <NavLink to="/dashboard/resumes">
            My Resumes
          </NavLink>

          <NavLink to="/dashboard/job-matching">
            Job Matching
          </NavLink>

          <NavLink to="/dashboard/account">
            My Account
          </NavLink>
        </nav>
      </aside>

      <main className="dashboard-main">
        <header className="dashboard-topbar">
          <h2>My Workspace</h2>
        </header>

        <div className="dashboard-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

export default DashboardLayout;