# ml-system

The `ml-system` module provides resume parsing, skill extraction, resume-to-job matching,
role benchmarks, skill-gap analysis, benchmark ranking, and a local HTTP service.

## Setup

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& ".\.venv\Scripts\Activate.ps1"
python -m pip install -r requirements.txt
```

## Run the CLI pipeline

Run the resume-to-job matcher:

```powershell
python run_pipeline.py "resume/tests/integration/fixtures/sample_resume.docx" `
  --job-description "Required: Python and Git. Preferred: Docker"
```

Rank a resume against the included role benchmarks:

```powershell
python run_pipeline.py "resume/tests/integration/fixtures/sample_resume.docx" `
  --benchmark-dir "datasets/role_benchmarks"
```

Add `--json` for machine-readable output or `--semantic` to include sentence-embedding similarity.

## Run the HTTP service

```powershell
python -m ml_service.server --host 127.0.0.1 --port 8000
```

`GET /health` verifies service availability.

`POST /score` accepts:

```json
{
  "resume_text": "Python and Git developer",
  "job_description": "Required: Python and Docker",
  "include_semantic": false
}
```

`POST /gap` accepts `resume_text` and a benchmark object with `benchmark_id`, `role`,
and `required_skills`.

`POST /rank` accepts `resume_text` and a non-empty `benchmarks` array.

## Tests

```powershell
python -m pytest -q
```
