from app.services.resume_processor import process_resume
from app.services.job_parser import parse_job_description
from app.services.job_skill_extractor import extract_job_skills
from app.services.keyword_matcher import calculate_keyword_match
from app.services.skill_matcher import calculate_skill_match
from app.services.job_semantic_matcher import calculate_job_semantic_match
from app.services.ats_scorer import calculate_ats_score
from app.services.job_matcher import generate_job_match


def analyze_resume_for_job(
    file_path: str,
    job_description: str
) -> dict:
    """
    Complete ATS analysis pipeline.
    """

    # 1. Process resume
    resume = process_resume(file_path)

    # 2. Parse job description
    job = parse_job_description(job_description)

    cleaned_job_description = job["cleaned_text"]

    # 3. Extract required job skills
    required_skills = extract_job_skills(
        cleaned_job_description
    )

    # 4. Collect resume skills
    resume_skills = []

    for skills in resume["skills"].values():
        resume_skills.extend(skills)

    # 5. Skill matching
    skill_result = calculate_skill_match(
        resume_skills,
        required_skills
    )

    # 6. Prepare resume text
    resume_text = "\n".join([
        resume["sections"]["experience"],
        resume["sections"]["skills"],
        resume["sections"]["projects"],
        resume["sections"]["education"],
        resume["sections"]["achievements"]
    ])

    # 7. Keyword matching
    keyword_result = calculate_keyword_match(
        resume_text,
        cleaned_job_description
    )

    # 8. Semantic matching
    semantic_similarity = calculate_job_semantic_match(
        resume_text,
        cleaned_job_description
    )

    # 9. ATS scoring
    ats_result = calculate_ats_score(
        skill_result["skill_match_percentage"],
        keyword_result["keyword_match_percentage"],
        semantic_similarity
    )

    # 10. Job match result
    match_result = generate_job_match(
        ats_result["ats_score"]
    )

    return {
        "job": job,
        "required_skills": required_skills,
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "skill_match_percentage":
            skill_result["skill_match_percentage"],
        "matched_keywords":
            keyword_result["matched_keywords"],
        "missing_keywords":
            keyword_result["missing_keywords"],
        "keyword_match_percentage":
            keyword_result["keyword_match_percentage"],
        "semantic_match_percentage":
            round(semantic_similarity * 100, 2),
        "ats_score":
            ats_result["ats_score"],
        "match_category":
            match_result["match_category"],
        "recommendation":
            match_result["recommendation"]
    }