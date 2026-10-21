
import { useRef, useState } from "react";
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
} from "lucide-react";
import "./ResumeUpload.css";

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB

function ResumeUpload() {
  const fileInputRef = useRef(null);
  const uploadTimerRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [status, setStatus] = useState("idle");
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");

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

    if (file.type !== "application/pdf" &&
        !file.name.toLowerCase().endsWith(".pdf")) {
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

    const file = event.dataTransfer.files?.[0];

    if (event.dataTransfer.files?.length > 1) {
      setError("Please select one resume at a time.");
      return;
    }

    handleFile(file);
  }

  function startUpload() {
    if (!selectedFile || status === "uploading") return;

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
        setStatus("success");
        return;
      }

      setProgress(currentProgress);
    }, 250);
  }

  const fileSize = selectedFile
    ? selectedFile.size < 1024 * 1024
      ? `${(selectedFile.size / 1024).toFixed(1)} KB`
      : `${(selectedFile.size / (1024 * 1024)).toFixed(2)} MB`
    : "";

  return (
    <section className="dashboard-page resume-upload-page">
      <div className="resume-page-heading">
        <div>
          <span className="resume-eyebrow">RESUME MANAGEMENT</span>
          <h1>My Resumes</h1>
          <p>
            Upload your resume and get ready to discover your career potential.
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
            <p>Start with a PDF resume. You can replace it whenever you need.</p>
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
              <strong title={selectedFile.name}>{selectedFile.name}</strong>
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

            {status === "uploading" ? (
              <span className="resume-progress-percent">{progress}%</span>
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
            Start demo upload
          </button>
        )}

        {status === "uploading" && (
          <div className="resume-uploading-note" role="status">
            <LoaderCircle size={17} className="resume-spinner" />
            Simulating upload progress…
          </div>
        )}

        {status === "success" && (
          <div className="resume-success-panel" role="status">
            <div className="resume-success-icon">
              <CheckCircle2 size={29} />
            </div>
            <h3>Demo upload complete!</h3>
            <p>
              Your resume passed the local checks. No file has been sent to a
              server yet.
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

      <div className="resume-info-grid">
        <article className="resume-info-card">
          <div className="resume-info-icon">
            <ShieldCheck size={22} />
          </div>
          <div>
            <h3>Your resume, your control</h3>
            <p>
              This demo validates the selected file in your browser. Server
              storage and account-based resume management will come later.
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
              Use a readable PDF with clear sections for skills, education,
              projects and experience.
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
