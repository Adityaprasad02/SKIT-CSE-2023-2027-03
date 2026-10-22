import { useState } from "react";
import { Link } from "react-router-dom";
import {
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
} from "lucide-react";

function Login() {
  const [showPassword, setShowPassword] = useState(false);

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));

    setErrors((previousErrors) => ({
      ...previousErrors,
      [name]: "",
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const newErrors = {};

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = "Email address is required.";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Please enter a valid email address.";
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = "Password is required.";
    }

    setErrors(newErrors);

    // Stop submission if there are errors
    if (Object.keys(newErrors).length > 0) {
      return;
    }

    // Temporary loading state
    setIsSubmitting(true);

    setTimeout(() => {
      console.log("Login form submitted:", formData);

      setIsSubmitting(false);
    }, 1000);
  };

  return (
    <div className="auth-card">

      {/* Header */}
      <div className="auth-header">

        <div className="auth-icon">
          <LockKeyhole size={24} />
        </div>

        <h1>Welcome Back</h1>

        <p>
          Login to your ResumeAI account
        </p>

      </div>

      {/* Login Form */}
      <form
        onSubmit={handleSubmit}
        className="auth-form"
        noValidate
      >

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

          <div className="password-label-row">

            <label htmlFor="password">
              Password
            </label>

            <Link to="/forgot-password">
              Forgot Password?
            </Link>

          </div>

          <div
            className={`input-wrapper ${
              errors.password ? "input-error" : ""
            }`}
          >

            <LockKeyhole size={19} />

            <input
              id="password"
              name="password"
              type={showPassword ? "text" : "password"}
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              autoComplete="current-password"
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

        {/* Submit */}
        <button
          type="submit"
          className="auth-submit-button"
          disabled={isSubmitting}
        >
          {isSubmitting
            ? "Logging in..."
            : "Login"}
        </button>

      </form>

      {/* Signup Link */}
      <div className="auth-switch">

        <p>
          Don't have an account?{" "}

          <Link to="/signup">
            Sign Up
          </Link>
        </p>

      </div>

    </div>
  );
}

export default Login;