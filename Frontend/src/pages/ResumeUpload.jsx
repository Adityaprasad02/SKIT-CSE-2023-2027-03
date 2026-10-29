
import { useEffect, useRef, useState } from "react";
import {
  Upload,
  FileText,
  FileCheck2,
  X,
  Trash2,
  CheckCircle2,
  AlertCircle,
  LoaderCircle,
  ArrowUpRight,
  ShieldCheck,
  Eye,
  CalendarDays,
} from "lucide-react";
import {
  saveResume,
  getAllResumes,
  getResumeById,
  deleteResume,
} from "../utils/resumeStorage";
import "./ResumeUpload.css";

const MAX_FILE_SIZE = 5 * 1024 * 1024;

function formatFileSize(bytes) {
  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

function formatUploadDate(date) {
  return new Date(date).toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function ResumeUpload() {
  const fileInputRef = useRef(null);
  const uploadTimerRef = useRef(null);
  const isMountedRef = useRef(true);

  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [status, setStatus] = useState("idle");
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");

  const [savedResumes, setSavedResumes] = useState([]);
  const [isLoadingResumes, setIsLoadingResumes] = useState(true);
  const [storageError, setStorageError] = useState("");
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    isMountedRef.current = true;

    async function loadResumes() {
      try {
        const resumes = await getAllResumes();

        if (isMountedRef.current) {
          setSavedResumes(resumes);
          setStorageError("");
        }
      } catch {
        if (isMountedRef.current) {
          setStorageError(
            "Could not access browser storage. Please check your browser settings and try again."
          );
        }
      } finally {
        if (isMountedRef.current) {
          setIsLoadingResumes(false);
        }
      }
    }

    loadResumes();

    return () => {
      isMountedRef.current = false;

      if (uploadTimerRef.current) {
        clearInterval(uploadTimerRef.current);
      }
    };
  }, []);

  function resetUpload() {
    if (uploadTimerRef.current) {
      clearInterval(uploadTimerRef.current);
      uploadTimerRef.current = null;
    }

    setSelectedFile(null);
    setStatus("idle");
    setProgress(0);
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  function handleFile(file) {
    if (!file) return;

    setError("");
    setProgress(0);

    if (
      file.type !== "application/pdf" &&
      !file.name.toLowerCase().endsWith(".pdf")
    ) {
      setError("Please select a PDF file.");
      return;
    }

    if (file.size === 0) {
      setError("This file is empty. Please choose another PDF.");
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      setError("File size must be 5 MB or less.");
      return;
    }

    if (uploadTimerRef.current) {
      clearInterval(uploadTimerRef.current);
      uploadTimerRef.current = null;
    }

    setSelectedFile(file);
    setStatus("ready");
  }

  function handleDrop(event) {
    event.preventDefault();
    setIsDragging(false);

    const files = event.dataTransfer.files;

    if (files.length > 1) {
      setError("Please select one resume at a time.");
      return;
    }

    handleFile(files[0]);
  }

  async function completeUpload(file) {
    try {
      const savedResume = await saveResume(file);

      if (!isMountedRef.current) return;

      setSavedResumes((current) => [
        savedResume,
        ...current.filter((resume) => resume.id !== savedResume.id),
      ]);

      setStatus("success");
      setProgress(100);
      setStorageError("");
    } catch {
      if (!isMountedRef.current) return;

      setStatus("ready");
      setProgress(0);
      setError(
        "The resume could not be saved in browser storage. Please try again."
      );
    }
  }

  function startUpload() {
    if (!selectedFile || status === "uploading" || status === "saving") {
      return;
    }

    const fileToSave = selectedFile;

    setError("");
    setProgress(0);
    setStatus("uploading");

    let currentProgress = 0;

    uploadTimerRef.current = setInterval(() => {
      currentProgress += Math.floor(Math.random() * 12) + 8;

      if (currentProgress >= 100) {
        currentProgress = 100;
        clearInterval(uploadTimerRef.current);
        uploadTimerRef.current = null;

        setProgress(100);
        setStatus("saving");
        void completeUpload(fileToSave);
        return;
      }

      setProgress(currentProgress);
    }, 250);
  }

  async function handleViewResume(resumeId) {
    // Open the tab during the click so browsers are less likely
    // to block it while the saved PDF is being retrieved.
    const pdfWindow = window.open("about:blank", "_blank");

    if (!pdfWindow) {
      setStorageError(
        "Your browser blocked the new tab. Allow pop-ups and try again."
      );
      return;
    }

    setStorageError("");

    try {
      const resume = await getResumeById(resumeId);

      if (!resume?.file) {
        pdfWindow.close();
        setStorageError("The saved PDF could not be found.");
        return;
      }

      const pdfUrl = URL.createObjectURL(resume.file);

      pdfWindow.opener = null;
      pdfWindow.location.href = pdfUrl;

      // Keep the URL alive while the browser loads the PDF.
      window.setTimeout(() => {
        URL.revokeObjectURL(pdfUrl);
      }, 60000);
    } catch {
      pdfWindow.close();
      setStorageError("Could not open this resume. Please try again.");
    }
  }

  async function handleDeleteResume(resume) {
    const confirmed = window.confirm(
      `Delete "${resume.name}" from this browser? This action cannot be undone.`
    );

    if (!confirmed) return;

    setDeletingId(resume.id);
    setStorageError("");

    try {
      await deleteResume(resume.id);

      if (!isMountedRef.current) return;

      setSavedResumes((current) =>
        current.filter((item) => item.id !== resume.id)
      );
    } catch {
      if (isMountedRef.current) {
        setStorageError("Could not delete the resume. Please try again.");
      }
    } finally {
      if (isMountedRef.current) {
        setDeletingId(null);
      }
    }
  }

  const fileSize = selectedFile
    ? formatFileSize(selectedFile.size)
    : "";

  return (
    <section className="dashboard-page resume-upload-page">
      <div className="resume-page-heading">
        <div>
          <span className="resume-eyebrow">RESUME MANAGEMENT</span>
          <h1>My Resumes</h1>
          <p>
            Upload, view and manage your resumes from one place.
          </p>
        </div>

        <div className="resume-heading-icon">
          <FileText size={27} />
        </div>
      </div>

      <div className="resume-upload-card">
        <div className="resume-card-heading">
          <div>
            <h2>Upload your resume</h2>
            <p>
              Choose a PDF resume. Your file will be saved in this browser.
            </p>
          </div>
          <span className="resume-format-badge">PDF ONLY</span>
        </div>

        {status !== "success" && (
          <div
            className={`resume-dropzone ${isDragging ? "is-dragging" : ""}`}
            onDragEnter={(event) => {
              event.preventDefault();
              setIsDragging(true);
            }}
            onDragOver={(event) => event.preventDefault()}
            onDragLeave={(event) => {
              if (!event.currentTarget.contains(event.relatedTarget)) {
                setIsDragging(false);
              }
            }}
            onDrop={handleDrop}
          >
            <input
              ref={fileInputRef}
              className="resume-file-input"
              type="file"
              accept=".pdf,application/pdf"
              aria-label="Choose a PDF resume"
              onChange={(event) => {
                handleFile(event.target.files?.[0]);
                event.target.value = "";
              }}
            />

            <div className="resume-upload-icon">
              <Upload size={28} />
            </div>

            <h3>Drag and drop your resume here</h3>
            <p>or choose a file from your computer</p>

            <button
              type="button"
              className="resume-browse-button"
              onClick={() => fileInputRef.current?.click()}
            >
              Browse files
              <ArrowUpRight size={17} />
            </button>

            <span className="resume-file-hint">
              PDF format · Maximum file size 5 MB
            </span>
          </div>
        )}

        {error && (
          <div className="resume-message resume-error" role="alert">
            <AlertCircle size={19} />
            <span>{error}</span>
          </div>
        )}

        {selectedFile && status !== "success" && (
          <div className="resume-selected-file">
            <div className="resume-file-icon">
              <FileText size={23} />
            </div>

            <div className="resume-file-info">
              <strong title={selectedFile.name}>
                {selectedFile.name}
              </strong>
              <span>{fileSize} · PDF document</span>

              {status === "uploading" && (
                <div
                  className="resume-progress-track"
                  role="progressbar"
                  aria-label="Demo upload progress"
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-valuenow={progress}
                >
                  <div
                    className="resume-progress-fill"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              )}
            </div>

            {status === "uploading" || status === "saving" ? (
              <span className="resume-progress-percent">
                {status === "saving" ? "Saving…" : `${progress}%`}
              </span>
            ) : (
              <button
                type="button"
                className="resume-remove-button"
                onClick={resetUpload}
                aria-label="Remove selected resume"
                title="Remove file"
              >
                <Trash2 size={18} />
              </button>
            )}
          </div>
        )}

        {status === "ready" && (
          <button
            type="button"
            className="resume-primary-button"
            onClick={startUpload}
          >
            <Upload size={18} />
            Save resume
          </button>
        )}

        {(status === "uploading" || status === "saving") && (
          <div className="resume-uploading-note" role="status">
            <LoaderCircle size={17} className="resume-spinner" />
            {status === "saving"
              ? "Saving PDF to browser storage…"
              : "Preparing your resume…"}
          </div>
        )}

        {status === "success" && (
          <div className="resume-success-panel" role="status">
            <div className="resume-success-icon">
              <CheckCircle2 size={29} />
            </div>
            <h3>Resume saved successfully!</h3>
            <p>
              Your PDF is saved in this browser. It has not been sent to
              a server or analyzed yet.
            </p>

            <div className="resume-success-file">
              <FileCheck2 size={22} />
              <div>
                <strong>{selectedFile.name}</strong>
                <span>{fileSize}</span>
              </div>
            </div>

            <button
              type="button"
              className="resume-primary-button"
              onClick={resetUpload}
            >
              <Upload size={18} />
              Upload another resume
            </button>
          </div>
        )}
      </div>

      <section className="saved-resumes-section">
        <div className="saved-resumes-heading">
          <div>
            <h2>Saved Resumes</h2>
            <p>
              {savedResumes.length}{" "}
              {savedResumes.length === 1 ? "resume" : "resumes"} stored
              in this browser
            </p>
          </div>

          <span className="saved-resumes-count">
            {savedResumes.length}
          </span>
        </div>

        {storageError && (
          <div className="resume-message resume-error" role="alert">
            <AlertCircle size={19} />
            <span>{storageError}</span>
          </div>
        )}

        {isLoadingResumes ? (
          <div className="saved-resumes-empty" role="status">
            <LoaderCircle size={24} className="resume-spinner" />
            <p>Loading saved resumes…</p>
          </div>
        ) : savedResumes.length === 0 ? (
          <div className="saved-resumes-empty">
            <div className="resume-upload-icon">
              <FileText size={27} />
            </div>
            <h3>No saved resumes yet</h3>
            <p>
              Your saved PDF resumes will appear here after you upload one.
            </p>
          </div>
        ) : (
          <div className="saved-resumes-list">
            {savedResumes.map((resume) => (
              <article className="saved-resume-item" key={resume.id}>
                <div className="resume-file-icon">
                  <FileCheck2 size={23} />
                </div>

                <div className="saved-resume-details">
                  <strong title={resume.name}>{resume.name}</strong>
                  <div className="saved-resume-meta">
                    <span>{formatFileSize(resume.size)}</span>
                    <span className="saved-resume-meta-separator">
                      ·
                    </span>
                    <span>
                      <CalendarDays size={14} />
                      {formatUploadDate(resume.uploadedAt)}
                    </span>
                  </div>
                  <span className="saved-resume-status">
                    <CheckCircle2 size={14} />
                    Saved locally
                  </span>
                </div>

                <div className="saved-resume-actions">
                  <button
                    type="button"
                    className="saved-resume-view"
                    onClick={() => handleViewResume(resume.id)}
                    aria-label={`View ${resume.name}`}
                  >
                    <Eye size={17} />
                    <span>View</span>
                  </button>

                  <button
                    type="button"
                    className="resume-remove-button"
                    onClick={() => handleDeleteResume(resume)}
                    disabled={deletingId === resume.id}
                    aria-label={`Delete ${resume.name}`}
                    title="Delete resume"
                  >
                    {deletingId === resume.id ? (
                      <LoaderCircle
                        size={18}
                        className="resume-spinner"
                      />
                    ) : (
                      <Trash2 size={18} />
                    )}
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      <div className="resume-info-grid">
        <article className="resume-info-card">
          <div className="resume-info-icon">
            <ShieldCheck size={22} />
          </div>
          <div>
            <h3>Your resume, your control</h3>
            <p>
              Files are stored in your browser, not on our server.
              Clearing browser data may remove them.
            </p>
          </div>
        </article>

        <article className="resume-info-card">
          <div className="resume-info-icon">
            <FileCheck2 size={22} />
          </div>
          <div>
            <h3>Make your resume ready</h3>
            <p>
              Use a readable PDF with clear sections for skills,
              education, projects and experience.
            </p>
          </div>
        </article>
      </div>

      <button
        type="button"
        className="resume-clear-button"
        onClick={resetUpload}
        disabled={!selectedFile && !error}
      >
        <X size={16} />
        Clear selection
      </button>
    </section>
  );
}

export default ResumeUpload;
