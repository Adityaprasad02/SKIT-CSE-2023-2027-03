import { Link, Outlet } from "react-router-dom";
import { FileText } from "lucide-react";

function AuthLayout() {
  return (
    <div className="auth-layout">

      <div className="auth-brand">
        <Link to="/" className="auth-logo">
          <FileText size={28} />
          <span>ResumeAI</span>
        </Link>
      </div>

      <main className="auth-content">
        <Outlet />
      </main>

      <div className="auth-footer">
        <p>
          © 2026 AI Resume Analyzer. All rights reserved.
        </p>
      </div>

    </div>
  );
}

export default AuthLayout;