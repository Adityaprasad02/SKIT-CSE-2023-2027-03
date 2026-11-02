
import { useEffect, useState } from "react";
import {
  BriefcaseBusiness,
  FileText,
  Target,
  CheckCircle2,
  AlertCircle,
  LoaderCircle,
  Sparkles,
  ArrowRight,
  Lightbulb,
  RotateCcw,
} from "lucide-react";

import { getAllResumes } from "../utils/resumeStorage";
import "./JobMatching.css";

const SAMPLE_DESCRIPTION = `We are looking for a Junior MERN Stack Developer.

Requirements:
- Strong knowledge of JavaScript and React
- Understanding of Node.js and Express.js
- Knowledge of MongoDB and REST APIs
- Familiarity with HTML, CSS and Git
- Problem-solving and communication skills
- Knowledge of data structures and algorithms`;

const DEMO_RESULTS = {
  score: 78,
  matchedSkills: [
    "JavaScript",
    "React",
    "HTML",
    "CSS",
    "Git",
  ],
  missingSkills: [
    "Node.js",
    "Express.js",
    "MongoDB",
    "REST APIs",
  ],
  suggestions: [
    "Strengthen your understanding of Node.js and Express.js.",
    "Build a small project using MongoDB and REST APIs.",
    "Highlight relevant projects and technical experience in your resume.",
  ],
};

function formatFileSize(bytes) {
  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

function JobMatching() {
  const [resumes, setResumes] = useState([]);
  const [selectedResumeId, setSelectedResumeId] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function loadResumes() {
      try {
        const savedResumes = await getAllResumes();

        if (isMounted) {
          setResumes(savedResumes);

          if (savedResumes.length > 0) {
            setSelectedResumeId(savedResumes[0].id);
          }
        }
      } catch {
        if (isMounted) {
          setError(
            "Could not load your saved resumes. Please try again."
          );
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadResumes();

    return () => {
      isMounted = false;
    };
  }, []);

  function handleAnalyze(event) {
    event.preventDefault();

    if (!selectedResumeId) {
      setError("Please select a resume first.");
      return;
    }

    if (jobDescription.trim().length < 50) {
      setError(
        "Please enter a job description containing at least 50 characters."
      );
      return;
    }

    setError("");
    setResults(null);
    setIsAnalyzing(true);

    // Demo-only result. Real resume analysis will be connected
    // to the backend in a future project milestone.
    window.setTimeout(() => {
      setResults(DEMO_RESULTS);
      setIsAnalyzing(false);
    }, 1200);
  }

  function handleReset() {
    setResults(null);
    setError("");
  }

  const selectedResume = resumes.find(
    (resume) => resume.id === selectedResumeId
  );

  return (
    <section className="dashboard-page job-matching-page">
      <div className="job-page-heading">
        <div>
          <span className="job-eyebrow">CAREER TOOLS</span>
          <h1>Job Matching</h1>
          <p>
            Compare your resume with job descriptions and discover
            opportunities to improve your profile.
          </p>
        </div>

        <div className="job-heading-icon">
          <Target size={28} />
        </div>
      </div>

      <div className="job-demo-notice">
        <Sparkles size={19} />
        <div>
          <strong>Demo mode</strong>
          <p>
            This version displays sample matching results.
            Real AI-powered resume analysis will be added
            after backend integration.
          </p>
        </div>
      </div>

      <form className="job-input-card" onSubmit={handleAnalyze}>
        <div className="job-card-heading">
          <div>
            <h2>Analyze a job opportunity</h2>
            <p>
              Select one of your saved resumes and provide
              the job description.
            </p>
          </div>

          <BriefcaseBusiness size={25} />
        </div>

        {error && (
          <div className="job-message job-error" role="alert">
            <AlertCircle size={19} />
            <span>{error}</span>
          </div>
        )}

        <div className="job-form-group">
          <label htmlFor="job-resume">Select your resume</label>

          {isLoading ? (
            <div className="job-loading-state">
              <LoaderCircle className="job-spinner" size={19} />
              Loading saved resumes...
            </div>
          ) : resumes.length === 0 ? (
            <div className="job-empty-resumes">
              <FileText size={21} />
              <div>
                <strong>No saved resumes found</strong>
                <p>
                  Upload a PDF resume before starting job matching.
                </p>
                <a href="/dashboard/resumes">
                  Go to My Resumes <ArrowRight size={15} />
                </a>
              </div>
            </div>
          ) : (
            <select
              id="job-resume"
              value={selectedResumeId}
              onChange={(event) => {
                setSelectedResumeId(event.target.value);
                setResults(null);
              }}
            >
              {resumes.map((resume) => (
                <option key={resume.id} value={resume.id}>
                  {resume.name} ({formatFileSize(resume.size)})
                </option>
              ))}
            </select>
          )}
        </div>

        {selectedResume && (
          <div className="job-selected-resume">
            <FileText size={21} />
            <div>
              <strong>{selectedResume.name}</strong>
              <span>
                {formatFileSize(selectedResume.size)} · Saved locally
              </span>
            </div>
            <CheckCircle2 size={19} />
          </div>
        )}

        <div className="job-form-group">
          <div className="job-label-row">
            <label htmlFor="job-description">
              Job description
            </label>

            <button
              type="button"
              className="job-sample-button"
              onClick={() => {
                setJobDescription(SAMPLE_DESCRIPTION);
                setResults(null);
                setError("");
              }}
            >
              Use sample description
            </button>
          </div>

          <textarea
            id="job-description"
            value={jobDescription}
            onChange={(event) => {
              setJobDescription(event.target.value);
              setResults(null);
              setError("");
            }}
            placeholder="Paste the complete job description here..."
            rows={9}
          />

          <span className="job-character-count">
            {jobDescription.length} characters · Minimum 50 characters
          </span>
        </div>

        <button
          type="submit"
          className="job-analyze-button"
          disabled={
            isLoading ||
            resumes.length === 0 ||
            isAnalyzing
          }
        >
          {isAnalyzing ? (
            <>
              <LoaderCircle className="job-spinner" size={19} />
              Preparing demo results...
            </>
          ) : (
            <>
              <Sparkles size={19} />
              Analyze Job Match
            </>
          )}
        </button>
      </form>

      {isAnalyzing && (
        <div className="job-analyzing-state" role="status">
          <LoaderCircle className="job-spinner" size={25} />
          <p>Preparing your sample matching results...</p>
        </div>
      )}

      {results && !isAnalyzing && (
        <section className="job-results-section">
          <div className="job-results-heading">
            <div>
              <span className="job-eyebrow">ANALYSIS PREVIEW</span>
              <h2>Job Match Results</h2>
              <p>
                Sample results for {selectedResume?.name}.
              </p>
            </div>

            <button
              type="button"
              className="job-reset-button"
              onClick={handleReset}
            >
              <RotateCcw size={16} />
              Reset
            </button>
          </div>

          <div className="job-score-card">
            <div className="job-score-icon">
              <Target size={25} />
            </div>

            <div className="job-score-content">
              <span>Sample Match Score</span>
              <strong>{results.score}%</strong>
              <p>
                Illustrative score only — not calculated
                from your actual PDF.
              </p>
            </div>

            <div
              className="job-score-progress"
              role="progressbar"
              aria-label="Sample match score"
              aria-valuemin={0}
              aria-valuemax={100}
              aria-valuenow={results.score}
            >
              <div
                style={{ width: `${results.score}%` }}
              />
            </div>
          </div>

          <div className="job-skill-grid">
            <article className="job-skill-card">
              <div className="job-skill-heading matched">
                <CheckCircle2 size={21} />
                <h3>Matched Skills</h3>
                <span>{results.matchedSkills.length}</span>
              </div>

              <div className="job-skill-list">
                {results.matchedSkills.map((skill) => (
                  <span key={skill}>{skill}</span>
                ))}
              </div>
            </article>

            <article className="job-skill-card">
              <div className="job-skill-heading missing">
                <AlertCircle size={21} />
                <h3>Skills to Improve</h3>
                <span>{results.missingSkills.length}</span>
              </div>

              <div className="job-skill-list missing-list">
                {results.missingSkills.map((skill) => (
                  <span key={skill}>{skill}</span>
                ))}
              </div>
            </article>
          </div>

          <article className="job-suggestions-card">
            <div className="job-suggestions-heading">
              <Lightbulb size={22} />
              <h3>Improvement Suggestions</h3>
            </div>

            <ul>
              {results.suggestions.map((suggestion) => (
                <li key={suggestion}>{suggestion}</li>
              ))}
            </ul>
          </article>
        </section>
      )}
    </section>
  );
}

export default JobMatching;
