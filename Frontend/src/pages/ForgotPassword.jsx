import { useState } from "react";
import { Link } from "react-router-dom";
import {
  KeyRound,
  Mail,
  ArrowLeft,
  CheckCircle2,
} from "lucide-react";

function ForgotPassword() {
  const [email, setEmail] = useState("");

  const [error, setError] = useState("");

  const [isSubmitting, setIsSubmitting] = useState(false);

  const [isSent, setIsSent] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();

    setError("");

    if (!email.trim()) {
      setError("Email address is required.");
      return;
    }

    if (!/\S+@\S+\.\S+/.test(email)) {
      setError("Please enter a valid email address.");
      return;
    }

    setIsSubmitting(true);

    setTimeout(() => {
      console.log(
        "Password reset requested for:",
        email
      );

      setIsSubmitting(false);
      setIsSent(true);
    }, 1000);
  };

  return (
    <div className="auth-card">

      {!isSent ? (
        <>
          {/* Header */}
          <div className="auth-header">

            <div className="auth-icon">
              <KeyRound size={24} />
            </div>

            <h1>Forgot Password?</h1>

            <p>
              Enter your email address and we'll help
              you reset your password.
            </p>

          </div>

          {/* Form */}
          <form
            onSubmit={handleSubmit}
            className="auth-form"
            noValidate
          >

            <div className="form-group">

              <label htmlFor="reset-email">
                Email Address
              </label>

              <div
                className={`input-wrapper ${
                  error ? "input-error" : ""
                }`}
              >

                <Mail size={19} />

                <input
                  id="reset-email"
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(event) => {
                    setEmail(event.target.value);
                    setError("");
                  }}
                  autoComplete="email"
                />

              </div>

              {error && (
                <span className="form-error">
                  {error}
                </span>
              )}

            </div>

            <button
              type="submit"
              className="auth-submit-button"
              disabled={isSubmitting}
            >
              {isSubmitting
                ? "Sending..."
                : "Send Reset Link"}
            </button>

          </form>

          {/* Back to Login */}
          <div className="auth-switch">

            <Link
              to="/login"
              className="back-to-login"
            >
              <ArrowLeft size={16} />
              Back to Login
            </Link>

          </div>
        </>
      ) : (
        /* Success State */
        <div className="reset-success">

          <div className="success-icon">
            <CheckCircle2 size={32} />
          </div>

          <h1>Check Your Email</h1>

          <p>
            If an account exists for{" "}
            <strong>{email}</strong>, you'll
            receive a password reset link shortly.
          </p>

          <Link
            to="/login"
            className="auth-submit-button success-button"
          >
            Back to Login
          </Link>

        </div>
      )}

    </div>
  );
}

export default ForgotPassword;