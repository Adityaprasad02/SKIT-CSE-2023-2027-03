"""
Classifies a detected header line (see header_detector.py) into a canonical
section type using sentence embeddings, instead of exact/fuzzy string
matching against a fixed keyword list.

Why embeddings instead of a keyword list:
  A resume might title its skills section "Skills", "Tech Stack",
  "Tools & Technologies", "Core Competencies", or something the taxonomy
  below never anticipated (e.g. "What I Bring To The Table"). A keyword
  list fails silently on anything not in it. Cosine similarity against a
  semantic anchor generalizes to unseen phrasing as long as it's roughly
  synonymous, and degrades gracefully (low similarity -> "other") instead
  of failing to match at all.

The lists of phrases below are NOT a matching dictionary — they're
training examples used once to compute an embedding centroid per section.
The actual comparison against a header is a similarity score, not
membership in these lists.
"""

from functools import lru_cache

CANONICAL_SECTIONS: dict[str, list[str]] = {
    "summary": [
        "career objective",
        "professional summary",
        "profile",
        "about me",
        "summary",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core competencies",
        "technologies",
        "tools and technologies",
        "tech stack",
    ],
    "education": [
        "education",
        "academic background",
        "qualifications",
        "academic qualifications",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "internship experience",
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "selected projects",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "licenses",
        "courses and certifications",
    ],
    "achievements": [
        "achievements",
        "awards",
        "honors",
        "accomplishments",
    ],
    "extracurricular": [
        "extracurricular activities",
        "volunteering",
        "leadership",
        "activities",
    ],
}

CLASSIFICATION_THRESHOLD = 0.45  # below this similarity -> "other"
_MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _get_model():
    """Lazy singleton so the (relatively heavy) embedding model is only
    loaded once per process, and only if section classification is
    actually used."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(_MODEL_NAME)


@lru_cache(maxsize=1)
def _get_section_centroids():
    """Embed every anchor phrase once and average per section to get one
    centroid vector per canonical section. Cached for process lifetime."""
    import numpy as np

    model = _get_model()
    centroids: dict[str, "np.ndarray"] = {}

    for section, phrases in CANONICAL_SECTIONS.items():
        embeddings = model.encode(phrases, normalize_embeddings=True)
        centroid = np.mean(embeddings, axis=0)
        # Averaging normalized vectors does not preserve unit length, and
        # the classifier below uses a plain dot product as a stand-in for
        # cosine similarity. Re-normalize or that comparison is skewed
        # toward centroids whose source phrases happened to agree less
        # (shorter mean vector) or more (longer mean vector).
        centroids[section] = centroid / np.linalg.norm(centroid)

    return centroids


def classify_header(header_text: str) -> tuple[str, float]:
    """Returns (section_name, similarity_score). section_name is 'other'
    when nothing clears CLASSIFICATION_THRESHOLD."""
    import numpy as np

    model = _get_model()
    centroids = _get_section_centroids()

    header_embedding = model.encode([header_text], normalize_embeddings=True)[0]

    best_section = "other"
    best_score = -1.0

    for section, centroid in centroids.items():
        score = float(np.dot(header_embedding, centroid))
        if score > best_score:
            best_section, best_score = section, score

    if best_score < CLASSIFICATION_THRESHOLD:
        return "other", best_score

    return best_section, best_score