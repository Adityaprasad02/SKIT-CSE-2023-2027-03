from __future__ import annotations

from typing import Protocol

import numpy as np


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class TextEncoder(Protocol):
    def encode(
        self,
        sentences: list[str],
        *,
        convert_to_numpy: bool,
        normalize_embeddings: bool,
    ) -> np.ndarray: ...


class SemanticMatcher:
    """Compare resume and job-description text using sentence embeddings."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        encoder: TextEncoder | None = None,
    ) -> None:
        if not model_name.strip():
            raise ValueError("model_name cannot be empty.")
        self.model_name = model_name
        self._encoder = encoder

    def _get_encoder(self) -> TextEncoder:
        if self._encoder is None:
            from sentence_transformers import SentenceTransformer

            self._encoder = SentenceTransformer(self.model_name)
        return self._encoder

    def score(self, resume_text: str, job_description: str) -> float:
        """Return clamped cosine similarity on a 0–100 scale, not a probability."""
        if not isinstance(resume_text, str) or not isinstance(job_description, str):
            raise TypeError("resume_text and job_description must be strings.")
        if not resume_text.strip() or not job_description.strip():
            return 0.0

        embeddings = np.asarray(
            self._get_encoder().encode(
                [resume_text, job_description],
                convert_to_numpy=True,
                normalize_embeddings=True,
            ),
            dtype=np.float64,
        )
        if (
            embeddings.ndim != 2
            or embeddings.shape[0] != 2
            or embeddings.shape[1] == 0
            or not np.isfinite(embeddings).all()
        ):
            raise ValueError("The encoder must return two finite embedding vectors.")

        resume_embedding, job_embedding = embeddings
        denominator = np.linalg.norm(resume_embedding) * np.linalg.norm(job_embedding)
        if denominator == 0:
            raise ValueError("The encoder must return non-zero embedding vectors.")

        cosine_similarity = float(np.dot(resume_embedding, job_embedding) / denominator)
        return round(min(100.0, max(0.0, cosine_similarity * 100.0)), 2)
