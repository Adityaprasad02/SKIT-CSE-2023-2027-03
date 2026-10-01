import numpy as np
import pytest
from unittest.mock import MagicMock, patch

from resume.preprocessing.section_classifier import (
    CANONICAL_SECTIONS,
    CLASSIFICATION_THRESHOLD,
    _get_section_centroids,
    classify_header,
)


# =========================================
# Canonical Sections Tests
# =========================================

def test_canonical_sections_exist():

    expected_sections = {
        "summary",
        "skills",
        "education",
        "experience",
        "projects",
        "certifications",
        "achievements",
        "extracurricular",
    }

    assert set(CANONICAL_SECTIONS.keys()) == expected_sections


def test_canonical_sections_have_anchor_phrases():

    for section, phrases in CANONICAL_SECTIONS.items():

        assert isinstance(section, str)
        assert len(phrases) > 0

        for phrase in phrases:
            assert isinstance(phrase, str)
            assert phrase


# =========================================
# _get_section_centroids() Tests
# =========================================

@patch(
    "resume.preprocessing.section_classifier._get_model"
)
def test_get_section_centroids_creates_centroid_for_each_section(
    mock_get_model
):

    _get_section_centroids.cache_clear()

    mock_model = MagicMock()

    mock_model.encode.return_value = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
    ])

    mock_get_model.return_value = mock_model

    centroids = _get_section_centroids()

    assert set(centroids.keys()) == set(
        CANONICAL_SECTIONS.keys()
    )


@patch(
    "resume.preprocessing.section_classifier._get_model"
)
def test_get_section_centroids_normalizes_centroids(
    mock_get_model
):

    _get_section_centroids.cache_clear()

    mock_model = MagicMock()

    mock_model.encode.return_value = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
    ])

    mock_get_model.return_value = mock_model

    centroids = _get_section_centroids()

    for centroid in centroids.values():

        norm = np.linalg.norm(centroid)

        assert norm == pytest.approx(1.0)


# =========================================
# classify_header() Tests
# =========================================

@patch(
    "resume.preprocessing.section_classifier._get_section_centroids"
)
@patch(
    "resume.preprocessing.section_classifier._get_model"
)
def test_classify_header_returns_best_section(
    mock_get_model,
    mock_get_centroids,
):

    mock_model = MagicMock()

    mock_model.encode.return_value = np.array([
        [1.0, 0.0]
    ])

    mock_get_model.return_value = mock_model

    mock_get_centroids.return_value = {
        "skills": np.array([1.0, 0.0]),
        "education": np.array([0.0, 1.0]),
    }

    section, score = classify_header(
        "TECHNICAL SKILLS"
    )

    assert section == "skills"
    assert score == 1.0


@patch(
    "resume.preprocessing.section_classifier._get_section_centroids"
)
@patch(
    "resume.preprocessing.section_classifier._get_model"
)
def test_classify_header_returns_highest_similarity(
    mock_get_model,
    mock_get_centroids,
):

    mock_model = MagicMock()

    mock_model.encode.return_value = np.array([
        [1.0, 0.0]
    ])

    mock_get_model.return_value = mock_model

    mock_get_centroids.return_value = {
        "skills": np.array([0.8, 0.0]),
        "education": np.array([0.9, 0.0]),
        "projects": np.array([0.7, 0.0]),
    }

    section, score = classify_header(
        "Some Header"
    )

    assert section == "education"
    assert score == pytest.approx(0.9)


@patch(
    "resume.preprocessing.section_classifier._get_section_centroids"
)
@patch(
    "resume.preprocessing.section_classifier._get_model"
)
def test_classify_header_returns_other_below_threshold(
    mock_get_model,
    mock_get_centroids,
):

    mock_model = MagicMock()

    mock_model.encode.return_value = np.array([
        [1.0, 0.0]
    ])

    mock_get_model.return_value = mock_model

    mock_get_centroids.return_value = {
        "skills": np.array([0.2, 0.0]),
        "education": np.array([0.3, 0.0]),
    }

    section, score = classify_header(
        "Random Header"
    )

    assert score < CLASSIFICATION_THRESHOLD
    assert section == "other"


@patch(
    "resume.preprocessing.section_classifier._get_section_centroids"
)
@patch(
    "resume.preprocessing.section_classifier._get_model"
)
def test_classify_header_accepts_score_equal_to_threshold(
    mock_get_model,
    mock_get_centroids,
):

    mock_model = MagicMock()

    mock_model.encode.return_value = np.array([
        [1.0, 0.0]
    ])

    mock_get_model.return_value = mock_model

    mock_get_centroids.return_value = {
        "skills": np.array([
            CLASSIFICATION_THRESHOLD,
            0.0,
        ]),
    }

    section, score = classify_header(
        "SKILLS"
    )

    assert score == CLASSIFICATION_THRESHOLD
    assert section == "skills"


@patch(
    "resume.preprocessing.section_classifier._get_section_centroids"
)
@patch(
    "resume.preprocessing.section_classifier._get_model"
)
def test_classify_header_encodes_header_correctly(
    mock_get_model,
    mock_get_centroids,
):

    mock_model = MagicMock()

    mock_model.encode.return_value = np.array([
        [1.0, 0.0]
    ])

    mock_get_model.return_value = mock_model

    mock_get_centroids.return_value = {
        "skills": np.array([1.0, 0.0]),
    }

    classify_header("TECH STACK")

    mock_model.encode.assert_called_once_with(
        ["TECH STACK"],
        normalize_embeddings=True,
    )