from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticAnalyzer:
    """
    Analyze semantic similarity between resume text
    and job description text.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def calculate_similarity(
        self,
        resume_text: str,
        job_description: str
    ) -> float:
        """
        Calculate semantic similarity between
        resume and job description.
        """

        if not resume_text.strip() or not job_description.strip():
            return 0.0

        embeddings = self.model.encode(
            [
                resume_text,
                job_description
            ]
        )

        similarity = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        return round(float(similarity), 4)