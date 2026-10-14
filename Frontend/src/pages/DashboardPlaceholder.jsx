import { useLocation, Link } from "react-router-dom";
import { ArrowLeft, FileSearch } from "lucide-react";

function DashboardPlaceholder() {
  const location = useLocation();

  const pageDetails = {
    "/dashboard/resumes": {
      title: "My Resumes",
      description:
        "Your uploaded resumes and analysis reports will appear here.",
    },
    "/dashboard/job-matching": {
      title: "Job Matching",
      description:
        "Discover job opportunities that match your skills and resume.",
    },
    "/dashboard/account": {
      title: "My Account",
      description:
        "Manage your profile and account settings here.",
    },
  };

  const currentPage = pageDetails[location.pathname] || {
    title: "Coming Soon",
    description: "This feature is currently under development.",
  };

  return (
    <section className="dashboard-page placeholder-page">
      <div className="placeholder-icon">
        <FileSearch size={30} />
      </div>

      <h1>{currentPage.title}</h1>
      <p>{currentPage.description}</p>

      <span className="coming-soon-label">
        Coming Soon
      </span>

      <Link to="/dashboard" className="placeholder-back-link">
        <ArrowLeft size={17} />
        Back to Overview
      </Link>
    </section>
  );
}

export default DashboardPlaceholder;