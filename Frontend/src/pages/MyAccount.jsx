
import { useState } from "react";
import {
  User,
  Mail,
  Phone,
  MapPin,
  Lock,
  ShieldCheck,
  Pencil,
  Save,
  X,
  CheckCircle2,
  Eye,
  EyeOff,
  CreditCard,
  Laptop,
} from "lucide-react";
import "./MyAccount.css";

const STORAGE_KEY = "resumeai-account-profile";

const defaultProfile = {
  name: "",
  email: "",
  phone: "",
  location: "",
};

const getSavedProfile = () => {
  try {
    const savedProfile = localStorage.getItem(STORAGE_KEY);

    return savedProfile
      ? { ...defaultProfile, ...JSON.parse(savedProfile) }
      : defaultProfile;
  } catch (error) {
    console.error("Unable to load profile:", error);
    return defaultProfile;
  }
};

const MyAccount = () => {
  const [profile, setProfile] = useState(getSavedProfile);
  const [draftProfile, setDraftProfile] = useState(getSavedProfile);
  const [isEditing, setIsEditing] = useState(false);

  const [profileMessage, setProfileMessage] = useState("");
  const [profileError, setProfileError] = useState(false);

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPasswords, setShowPasswords] = useState(false);

  const [passwordMessage, setPasswordMessage] = useState("");
  const [passwordError, setPasswordError] = useState(false);

  const getInitials = (name) => {
    if (!name.trim()) return "U";

    return name
      .trim()
      .split(/\s+/)
      .slice(0, 2)
      .map((part) => part[0].toUpperCase())
      .join("");
  };

  const handleEdit = () => {
    setDraftProfile({ ...profile });
    setIsEditing(true);
    setProfileMessage("");
    setProfileError(false);
  };

  const handleCancel = () => {
    setDraftProfile({ ...profile });
    setIsEditing(false);
    setProfileMessage("");
    setProfileError(false);
  };

  const handleProfileChange = (event) => {
    const { name, value } = event.target;

    setDraftProfile((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleProfileSave = (event) => {
    event.preventDefault();

    setProfileMessage("");
    setProfileError(false);

    if (!draftProfile.name.trim() || !draftProfile.email.trim()) {
      setProfileMessage("Name and email are required.");
      setProfileError(true);
      return;
    }

    try {
      const updatedProfile = {
        name: draftProfile.name.trim(),
        email: draftProfile.email.trim(),
        phone: draftProfile.phone.trim(),
        location: draftProfile.location.trim(),
      };

      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(updatedProfile)
      );

      setProfile(updatedProfile);
      setDraftProfile(updatedProfile);
      setIsEditing(false);
      setProfileMessage("Profile updated successfully.");
    } catch (error) {
      console.error("Unable to save profile:", error);
      setProfileMessage("Unable to save your profile in this browser.");
      setProfileError(true);
    }
  };

  const handlePasswordChange = (event) => {
    event.preventDefault();

    setPasswordMessage("");
    setPasswordError(false);

    if (!currentPassword || !newPassword || !confirmPassword) {
      setPasswordMessage("Please fill in all password fields.");
      setPasswordError(true);
      return;
    }

    if (newPassword.length < 8) {
      setPasswordMessage(
        "New password must contain at least 8 characters."
      );
      setPasswordError(true);
      return;
    }

    if (newPassword !== confirmPassword) {
      setPasswordMessage("New passwords do not match.");
      setPasswordError(true);
      return;
    }

    setPasswordMessage(
      "This is a frontend demo. Password changes will be enabled after backend integration."
    );

    setCurrentPassword("");
    setNewPassword("");
    setConfirmPassword("");
  };

  return (
    <div className="account-page">
      {/* Page Header */}
      <div className="account-page-heading">
        <div>
          <span className="account-eyebrow">ACCOUNT SETTINGS</span>
          <h1>My Account</h1>
          <p>Manage your personal information and account preferences.</p>
        </div>

        <div className="account-status">
          <span className="account-status-dot" />
          Active Account
        </div>
      </div>

      {/* Two Column Layout */}
      <div className="account-grid">

        {/* LEFT COLUMN */}
        <div className="account-main-column">

          {/* Profile Overview */}
          <section className="account-card account-profile-overview">
            <div className="account-avatar">
              {getInitials(profile.name)}
            </div>

            <div className="account-profile-summary">
              <h2>{profile.name || "Your Name"}</h2>
              <p>{profile.email || "Add your email address"}</p>

              <span>
                <ShieldCheck size={14} />
                Free Member
              </span>
            </div>

            {!isEditing && (
              <button
                type="button"
                className="account-outline-button"
                onClick={handleEdit}
              >
                <Pencil size={16} />
                Edit Profile
              </button>
            )}
          </section>

          {/* Personal Information */}
          <section className="account-card">
            <div className="account-section-heading">
              <div>
                <h2>Personal Information</h2>
                <p>Update your personal details here.</p>
              </div>
            </div>

            <form onSubmit={handleProfileSave}>
              <div className="account-fields-grid">

                <div className="account-field">
                  <label htmlFor="account-name">
                    Full Name
                  </label>

                  <div className={`account-input-wrapper ${isEditing ? "is-editing" : ""}`}>
                    <User size={17} />

                    <input
                      id="account-name"
                      type="text"
                      name="name"
                      placeholder="Enter your full name"
                      value={draftProfile.name}
                      onChange={handleProfileChange}
                      readOnly={!isEditing}
                      required
                    />
                  </div>
                </div>

                <div className="account-field">
                  <label htmlFor="account-email">
                    Email Address
                  </label>

                  <div className={`account-input-wrapper ${isEditing ? "is-editing" : ""}`}>
                    <Mail size={17} />

                    <input
                      id="account-email"
                      type="email"
                      name="email"
                      placeholder="Enter your email"
                      value={draftProfile.email}
                      onChange={handleProfileChange}
                      readOnly={!isEditing}
                      required
                    />
                  </div>
                </div>

                <div className="account-field">
                  <label htmlFor="account-phone">
                    Phone Number
                  </label>

                  <div className={`account-input-wrapper ${isEditing ? "is-editing" : ""}`}>
                    <Phone size={17} />

                    <input
                      id="account-phone"
                      type="tel"
                      name="phone"
                      placeholder="Enter your phone number"
                      value={draftProfile.phone}
                      onChange={handleProfileChange}
                      readOnly={!isEditing}
                    />
                  </div>
                </div>

                <div className="account-field">
                  <label htmlFor="account-location">
                    Location
                  </label>

                  <div className={`account-input-wrapper ${isEditing ? "is-editing" : ""}`}>
                    <MapPin size={17} />

                    <input
                      id="account-location"
                      type="text"
                      name="location"
                      placeholder="Enter your location"
                      value={draftProfile.location}
                      onChange={handleProfileChange}
                      readOnly={!isEditing}
                    />
                  </div>
                </div>
              </div>

              {profileMessage && (
                <p
                  className={`account-feedback ${
                    profileError
                      ? "account-feedback-error"
                      : "account-feedback-success"
                  }`}
                  role={profileError ? "alert" : "status"}
                >
                  {profileError ? (
                    <X size={17} />
                  ) : (
                    <CheckCircle2 size={17} />
                  )}
                  {profileMessage}
                </p>
              )}

              {isEditing && (
                <div className="account-form-actions">
                  <button
                    type="button"
                    className="account-cancel-button"
                    onClick={handleCancel}
                  >
                    <X size={16} />
                    Cancel
                  </button>

                  <button
                    type="submit"
                    className="account-primary-button"
                  >
                    <Save size={16} />
                    Save Changes
                  </button>
                </div>
              )}
            </form>
          </section>

          {/* Password & Security */}
          <section className="account-card">
            <div className="account-section-heading">
              <div>
                <h2>Password & Security</h2>
                <p>Manage your account password.</p>
              </div>
            </div>

            <form
              className="account-password-form"
              onSubmit={handlePasswordChange}
            >
              <div className="account-fields-grid">

                <div className="account-field">
                  <label htmlFor="current-password">
                    Current Password
                  </label>

                  <input
                    className="account-password-input"
                    id="current-password"
                    type={showPasswords ? "text" : "password"}
                    placeholder="Enter current password"
                    value={currentPassword}
                    onChange={(event) =>
                      setCurrentPassword(event.target.value)
                    }
                  />
                </div>

                <div className="account-field">
                  <label htmlFor="new-password">
                    New Password
                  </label>

                  <input
                    className="account-password-input"
                    id="new-password"
                    type={showPasswords ? "text" : "password"}
                    placeholder="Enter new password"
                    value={newPassword}
                    onChange={(event) =>
                      setNewPassword(event.target.value)
                    }
                  />
                </div>

                <div className="account-field">
                  <label htmlFor="confirm-password">
                    Confirm New Password
                  </label>

                  <input
                    className="account-password-input"
                    id="confirm-password"
                    type={showPasswords ? "text" : "password"}
                    placeholder="Confirm new password"
                    value={confirmPassword}
                    onChange={(event) =>
                      setConfirmPassword(event.target.value)
                    }
                  />
                </div>
              </div>

              <button
                type="button"
                className="account-password-toggle"
                onClick={() =>
                  setShowPasswords((previous) => !previous)
                }
              >
                {showPasswords ? (
                  <EyeOff size={16} />
                ) : (
                  <Eye size={16} />
                )}

                {showPasswords ? "Hide passwords" : "Show passwords"}
              </button>

              {passwordMessage && (
                <p
                  className={`account-feedback ${
                    passwordError
                      ? "account-feedback-error"
                      : "account-feedback-success"
                  }`}
                  role={passwordError ? "alert" : "status"}
                >
                  {passwordError ? (
                    <X size={17} />
                  ) : (
                    <CheckCircle2 size={17} />
                  )}
                  {passwordMessage}
                </p>
              )}

              <button
                type="submit"
                className="account-primary-button"
              >
                <Lock size={16} />
                Update Password
              </button>
            </form>

            <div className="account-demo-notice">
              <ShieldCheck size={18} />
              <p>
                Password updates are currently displayed as a frontend
                demo. Real authentication and password changes will
                be connected during backend integration.
              </p>
            </div>
          </section>
        </div>

        {/* RIGHT COLUMN */}
        <aside className="account-side-column">

          {/* Account Information */}
          <section className="account-card account-details-card">
            <div className="account-section-heading">
              <div>
                <h2>Account Information</h2>
                <p>Basic details about your account.</p>
              </div>
            </div>

            <div className="account-detail-item">
              <div className="account-detail-icon">
                <ShieldCheck size={19} />
              </div>

              <div>
                <span>Account Status</span>
                <strong className="account-status-active">
                  Active
                </strong>
              </div>
            </div>

            <div className="account-detail-item">
              <div className="account-detail-icon">
                <CreditCard size={19} />
              </div>

              <div>
                <span>Membership Plan</span>
                <strong>Free Plan</strong>
              </div>
            </div>

            <div className="account-detail-item">
              <div className="account-detail-icon">
                <Laptop size={19} />
              </div>

              <div>
                <span>Platform</span>
                <strong>ResumeAI</strong>
              </div>
            </div>
          </section>

          {/* Help & Privacy */}
          <section className="account-help-card">
            <div className="account-help-icon">
              <ShieldCheck size={22} />
            </div>

            <h3>Your Privacy Matters</h3>

            <p>
              Your profile details are currently stored locally in
              this browser using localStorage. Server-side account
              management will be available after backend integration.
            </p>
          </section>
        </aside>
      </div>
    </div>
  );
};

export default MyAccount;
