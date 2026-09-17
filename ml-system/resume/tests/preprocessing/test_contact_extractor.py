from resume.preprocessing.contact_extractor import extract_contact_info


# =========================================
# Email Tests
# =========================================

def test_extract_single_email():

    text = "Contact me at aditya@example.com"

    result = extract_contact_info(text)

    assert result.emails == ["aditya@example.com"]


def test_extract_multiple_emails():

    text = """
    aditya@example.com
    test.user@gmail.com
    """

    result = extract_contact_info(text)

    assert result.emails == [
        "aditya@example.com",
        "test.user@gmail.com",
    ]


def test_extract_duplicate_emails():

    text = """
    aditya@example.com
    aditya@example.com
    """

    result = extract_contact_info(text)

    assert result.emails == ["aditya@example.com"]


# =========================================
# Phone Tests
# =========================================

def test_extract_phone_number():

    text = "Phone: 9876543210"

    result = extract_contact_info(text)

    assert result.phones == ["9876543210"]


def test_extract_phone_with_country_code():

    text = "Phone: +91 9876543210"

    result = extract_contact_info(text)

    assert result.phones == ["+91 9876543210"]


def test_extract_duplicate_phone_numbers():

    text = """
    9876543210
    9876543210
    """

    result = extract_contact_info(text)

    assert result.phones == ["9876543210"]


# =========================================
# LinkedIn Tests
# =========================================

def test_extract_linkedin_url():

    text = "linkedin.com/in/aditya-singh"

    result = extract_contact_info(text)

    assert result.linkedin == [
        "linkedin.com/in/aditya-singh"
    ]


def test_extract_linkedin_with_https():

    text = "https://www.linkedin.com/in/aditya-singh"

    result = extract_contact_info(text)

    assert result.linkedin == [
        "https://www.linkedin.com/in/aditya-singh"
    ]


def test_extract_duplicate_linkedin():

    text = """
    linkedin.com/in/aditya-singh
    linkedin.com/in/aditya-singh
    """

    result = extract_contact_info(text)

    assert result.linkedin == [
        "linkedin.com/in/aditya-singh"
    ]


# =========================================
# GitHub Tests
# =========================================

def test_extract_github_url():

    text = "github.com/adityasingh"

    result = extract_contact_info(text)

    assert result.github == [
        "github.com/adityasingh"
    ]


def test_extract_github_with_https():

    text = "https://github.com/adityasingh"

    result = extract_contact_info(text)

    assert result.github == [
        "https://github.com/adityasingh"
    ]


def test_extract_duplicate_github():

    text = """
    github.com/adityasingh
    github.com/adityasingh
    """

    result = extract_contact_info(text)

    assert result.github == [
        "github.com/adityasingh"
    ]


# =========================================
# Empty Contact Tests
# =========================================

def test_extract_contact_info_with_no_contacts():

    text = "Python Developer with Machine Learning experience"

    result = extract_contact_info(text)

    assert result.emails == []
    assert result.phones == []
    assert result.linkedin == []
    assert result.github == []


# =========================================
# Combined Contact Tests
# =========================================

def test_extract_all_contact_information():

    text = """
    Aditya Singh

    Email: aditya@example.com
    Phone: 9876543210

    LinkedIn:
    linkedin.com/in/aditya-singh

    GitHub:
    github.com/adityasingh
    """

    result = extract_contact_info(text)

    assert result.emails == ["aditya@example.com"]

    assert result.phones == ["9876543210"]

    assert result.linkedin == [
        "linkedin.com/in/aditya-singh"
    ]

    assert result.github == [
        "github.com/adityasingh"
    ]