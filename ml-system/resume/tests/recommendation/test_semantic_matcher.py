import numpy as np
import pytest

from recommendation import SemanticMatcher


class StubEncoder:
    def __init__(self, embeddings: np.ndarray) -> None:
        self.embeddings = embeddings
        self.calls: list[list[str]] = []

    def encode(
        self,
        sentences: list[str],
        *,
        convert_to_numpy: bool,
        normalize_embeddings: bool,
    ) -> np.ndarray:
        assert convert_to_numpy
        assert normalize_embeddings
        self.calls.append(sentences)
        return self.embeddings


def test_semantic_matcher_returns_cosine_similarity_as_percentage():
    encoder = StubEncoder(np.array([[1.0, 0.0], [0.6, 0.8]]))

    score = SemanticMatcher(encoder=encoder).score(
        "Python developer",
        "Looking for a Python engineer",
    )

    assert score == 60.0
    assert encoder.calls == [["Python developer", "Looking for a Python engineer"]]


def test_semantic_matcher_clamps_negative_similarity_to_zero():
    encoder = StubEncoder(np.array([[1.0, 0.0], [-1.0, 0.0]]))

    assert SemanticMatcher(encoder=encoder).score("resume", "job") == 0.0


def test_semantic_matcher_does_not_encode_empty_text():
    encoder = StubEncoder(np.array([[1.0, 0.0], [0.0, 1.0]]))

    assert SemanticMatcher(encoder=encoder).score("  ", "job") == 0.0
    assert encoder.calls == []


def test_semantic_matcher_rejects_invalid_embedding_output():
    encoder = StubEncoder(np.array([[1.0, 0.0]]))

    with pytest.raises(ValueError, match="two finite embedding vectors"):
        SemanticMatcher(encoder=encoder).score("resume", "job")


def test_semantic_matcher_rejects_non_string_text():
    with pytest.raises(TypeError, match="must be strings"):
        SemanticMatcher(encoder=StubEncoder(np.eye(2))).score(None, "job")


def test_semantic_matcher_rejects_empty_model_name():
    with pytest.raises(ValueError, match="model_name"):
        SemanticMatcher(model_name=" ")
