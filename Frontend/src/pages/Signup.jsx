import { useState } from "react";
import { Link } from "react-router-dom";
import {
  User,
  Mail,
  LockKeyhole,
  Eye,
  EyeOff,
  UserPlus,
} from "lucide-react";

function Signup() {
  const [showPassword, setShowPassword] = useState(false);

  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    terms: false,
  });

  const [errors, setErrors] = useState({});

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]:
        type === "checkbox"
          ? checked
          : value,
    }));

    setErrors((previousErrors) => ({
      ...previousErrors,
      [name]: "",
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const newErrors = {};

    // Name validation
    if (!formData.name.trim()) {
      newErrors.name = "Full name is required.";
    }

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = "Email address is required.";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Please enter a valid email address.";
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = "Password is required.";
    } else if (formData.password.length < 6) {
      newErrors.password =
        "Password must contain at least 6 characters.";
    }

    // Confirm password validation
    if (!formData.confirmPassword) {
      newErrors.confirmPassword =
        "Please confirm your password.";
    } else if (
      formData.password !== formData.confirmPassword
    ) {
      newErrors.confirmPassword =
        "Passwords do not match.";
    }

    // Terms validation
    if (!formData.terms) {
      newErrors.terms =
        "You must accept the Terms & Conditions.";
    }

    setErrors(newErrors);

    // Stop submission if errors exist
    if (Object.keys(newErrors).length > 0) {
      return;
    }

    // Temporary loading state
    setIsSubmitting(true);

    setTimeout(() => {
      console.log(
        "Signup form submitted:",
        formData
      );

      setIsSubmitting(false);
    }, 1000);
  };

  return (
    <div className="auth-card signup-card">

      {/* Header */}
      <div className="auth-header">

        <div className="auth-icon">
          <UserPlus size={24} />
        </div>

        <h1>Create Account</h1>

        <p>
          Start analyzing your resume with ResumeAI
        </p>

      </div>

      {/* Signup Form */}
      <form
        onSubmit={handleSubmit}
        className="auth-form"
        noValidate
      >

        {/* Full Name */}
        <div className="form-group">

          <label htmlFor="name">
            Full Name
          </label>

          <div
            className={`input-wrapper ${
              errors.name ? "input-error" : ""
            }`}
          >

            <User size={19} />

            <input
              id="name"
              name="name"
              type="text"
              placeholder="Enter your full name"
              value={formData.name}
              onChange={handleChange}
              autoComplete="name"
            />

          </div>

          {errors.name && (
            <span className="form-error">
              {errors.name}
            </span>
          )}

        </div>

        {/* Email */}
        <div className="form-group">

          <label htmlFor="email">
            Email Address
          </label>

          <div
            className={`input-wrapper ${
              errors.email ? "input-error" : ""
            }`}
          >

            <Mail size={19} />

            <input
              id="email"
              name="email"
              type="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              autoComplete="email"
            />

          </div>

          {errors.email && (
            <span className="form-error">
              {errors.email}
            </span>
          )}

        </div>

        {/* Password */}
        <div className="form-group">

          <label htmlFor="password">
            Password
          </label>

          <div
            className={`input-wrapper ${
              errors.password ? "input-error" : ""
            }`}
          >

            <LockKeyhole size={19} />

            <input
              id="password"
              name="password"
              type={
                showPassword
                  ? "text"
                  : "password"
              }
              placeholder="Create a password"
              value={formData.password}
              onChange={handleChange}
              autoComplete="new-password"
            />

            <button
              type="button"
              className="password-toggle"
              onClick={() =>
                setShowPassword(!showPassword)
              }
              aria-label={
                showPassword
                  ? "Hide password"
                  : "Show password"
              }
            >
              {showPassword ? (
                <EyeOff size={19} />
              ) : (
                <Eye size={19} />
              )}
            </button>

          </div>

          {errors.password && (
            <span className="form-error">
              {errors.password}
            </span>
          )}

        </div>

        {/* Confirm Password */}
        <div className="form-group">

          <label htmlFor="confirmPassword">
            Confirm Password
          </label>

          <div
            className={`input-wrapper ${
              errors.confirmPassword
                ? "input-error"
                : ""
            }`}
          >

            <LockKeyhole size={19} />

            <input
              id="confirmPassword"
              name="confirmPassword"
              type={
                showConfirmPassword
                  ? "text"
                  : "password"
              }
              placeholder="Confirm your password"
              value={formData.confirmPassword}
              onChange={handleChange}
              autoComplete="new-password"
            />

            <button
              type="button"
              className="password-toggle"
              onClick={() =>
                setShowConfirmPassword(
                  !showConfirmPassword
                )
              }
              aria-label={
                showConfirmPassword
                  ? "Hide confirm password"
                  : "Show confirm password"
              }
            >
              {showConfirmPassword ? (
                <EyeOff size={19} />
              ) : (
                <Eye size={19} />
              )}
            </button>

          </div>

          {errors.confirmPassword && (
            <span className="form-error">
              {errors.confirmPassword}
            </span>
          )}

        </div>

        {/* Terms */}
        <div className="terms-section">

          <div className="terms-group">

            <input
              id="terms"
              name="terms"
              type="checkbox"
              checked={formData.terms}
              onChange={handleChange}
            />

            <label htmlFor="terms">
              I agree to the{" "}
              <a href="#terms">
                Terms & Conditions
              </a>
            </label>

          </div>

          {errors.terms && (
            <span className="form-error">
              {errors.terms}
            </span>
          )}

        </div>

        {/* Submit */}
        <button
          type="submit"
          className="auth-submit-button"
          disabled={isSubmitting}
        >
          {isSubmitting
            ? "Creating Account..."
            : "Create Account"}
        </button>

      </form>

      {/* Login Link */}
      <div className="auth-switch">

        <p>
          Already have an account?{" "}

          <Link to="/login">
            Login
          </Link>
        </p>

      </div>

    </div>
  );
}

export default Signup;