import { Link } from "react-router-dom";
import { FileText } from "lucide-react";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">

        {/* Logo */}
        <Link to="/" className="logo">
          <FileText size={24} />
          <span>ResumeAI</span>
        </Link>

        {/* Navigation Links */}
        <div className="nav-links">
          <Link to="/">Home</Link>
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
        </div>

        {/* Authentication */}
        <div className="nav-actions">
          <Link to="/login" className="login-link">
            Login
          </Link>

          <Link to="/signup" className="signup-button">
            Sign Up
          </Link>
        </div>

      </div>
    </nav>
  );
}

export default Navbar;