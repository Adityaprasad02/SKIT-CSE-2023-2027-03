import pytest

from resume.preprocessing.text_cleaner import clean_text


# =========================================
# Input Validation Tests
# =========================================

def test_clean_text_rejects_non_string():

    with pytest.raises(TypeError, match="Input text must be a string"):
        clean_text(123)


# =========================================
# Unicode Normalization Tests
# =========================================

def test_clean_text_normalizes_unicode():

    text = "Python ＋ Machine Learning"

    result = clean_text(text)

    assert result == "Python + Machine Learning"


# =========================================
# Line Ending Tests
# =========================================

def test_clean_text_normalizes_windows_line_endings():

    text = "Python\r\nMachine Learning"

    result = clean_text(text)

    assert result == "Python\nMachine Learning"


def test_clean_text_normalizes_old_mac_line_endings():

    text = "Python\rMachine Learning"

    result = clean_text(text)

    assert result == "Python\nMachine Learning"


# =========================================
# Space Handling Tests
# =========================================

def test_clean_text_replaces_non_breaking_space():

    text = "Python\u00A0Developer"

    result = clean_text(text)

    assert result == "Python Developer"


def test_clean_text_removes_excessive_spaces():

    text = "Python     Machine     Learning"

    result = clean_text(text)

    assert result == "Python Machine Learning"


def test_clean_text_replaces_tabs():

    text = "Python\t\tMachine\tLearning"

    result = clean_text(text)

    assert result == "Python Machine Learning"


def test_clean_text_strips_line_whitespace():

    text = "   Python Developer   "

    result = clean_text(text)

    assert result == "Python Developer"


# =========================================
# Invisible Character Tests
# =========================================

def test_clean_text_removes_zero_width_space():

    text = "Python\u200BDeveloper"

    result = clean_text(text)

    assert result == "PythonDeveloper"


def test_clean_text_removes_zero_width_non_joiner():

    text = "Python\u200CDeveloper"

    result = clean_text(text)

    assert result == "PythonDeveloper"


def test_clean_text_removes_zero_width_joiner():

    text = "Python\u200DDeveloper"

    result = clean_text(text)

    assert result == "PythonDeveloper"


def test_clean_text_removes_zero_width_no_break_space():

    text = "Python\uFEFFDeveloper"

    result = clean_text(text)

    assert result == "PythonDeveloper"


# =========================================
# Empty Line Tests
# =========================================

def test_clean_text_limits_consecutive_empty_lines():

    text = "Python\n\n\n\nMachine Learning"

    result = clean_text(text)

    assert result == "Python\n\nMachine Learning"


# =========================================
# Content Preservation Tests
# =========================================

def test_clean_text_preserves_technical_characters():

    text = "C++ C# Node.js Python 3.12"

    result = clean_text(text)

    assert result == "C++ C# Node.js Python 3.12"


def test_clean_text_preserves_case():

    text = "Python Machine Learning API"

    result = clean_text(text)

    assert result == "Python Machine Learning API"


def test_clean_text_preserves_numbers():

    text = "Python 3.12"

    result = clean_text(text)

    assert result == "Python 3.12"