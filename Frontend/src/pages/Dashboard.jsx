import { FileText, Target, Briefcase, Upload, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

function Dashboard() {
  const stats = [
    {
      title: "Resumes Analyzed",
      value: "0",
      description: "Start by uploading your resume",
      icon: FileText,
      color: "blue",
    },
    {
      title: "Average ATS Score",
      value: "--",
      description: "Your average score will appear here",
      icon: Target,
      color: "purple",
    },
    {
      title: "Job Matches",
      value: "0",
      description: "Discover jobs matching your profile",
      icon: Briefcase,
      color: "green",
    },
  ];

  return (
    <section className="dashboard-page">
      {/* Welcome Section */}
      <div className="dashboard-welcome">
        <h1>Welcome to your dashboard!</h1>
        <p>
          Manage your resumes and track your progress
          from one place.
        </p>
      </div>

      {/* Overview Cards */}
      <div className="dashboard-stats">
        {stats.map((stat) => {
          const Icon = stat.icon;

          return (
            <article
              className="dashboard-stat-card"
              key={stat.title}
            >
              <div className="dashboard-stat-top">
                <div
                  className={`dashboard-stat-icon ${stat.color}`}
                >
                  <Icon size={22} />
                </div>

                <span className="dashboard-stat-title">
                  {stat.title}
                </span>
              </div>

              <h2>{stat.value}</h2>
              <p>{stat.description}</p>
            </article>
          );
        })}
      </div>

      {/* Recent Analyses */}
      <section className="recent-analyses">
        <div className="recent-analyses-header">
          <div>
            <h2>Recent Analyses</h2>
            <p>Review your recently analyzed resumes.</p>
          </div>

          <Link
            to="/dashboard/resumes"
            className="view-all-link"
          >
            View all <ArrowRight size={16} />
          </Link>
        </div>

        <div className="recent-analyses-empty">
          <div className="empty-state-icon">
            <FileText size={30} />
          </div>

          <h3>No analyses yet</h3>

          <p>
            Upload your first resume to get your ATS score
            and personalized improvement suggestions.
          </p>

          <Link
            to="/dashboard/resumes"
            className="upload-resume-button"
          >
            <Upload size={18} />
            Upload Resume
          </Link>
        </div>
      </section>
    </section>
  );
}

export default Dashboard;