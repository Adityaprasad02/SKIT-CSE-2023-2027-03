from app.services.semantic_analyzer import SemanticAnalyzer


def calculate_job_semantic_match(
    resume_text: str,
    job_description: str
) -> float:
    """
    Calculate semantic similarity between
    a resume and a job description.
    """

    analyzer = SemanticAnalyzer()

    similarity = analyzer.calculate_similarity(
        resume_text,
        job_description
    )

    return similarity