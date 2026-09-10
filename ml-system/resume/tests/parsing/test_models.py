from resume.parsing.models import RawLine


def test_raw_line_creation():
    line = RawLine(
        text="Python Developer",
        page_number=1,
        font_size=14.0,
        is_bold=True,
        is_italic=False,
        line_index=0,
    )

    assert line.text == "Python Developer"
    assert line.page_number == 1
    assert line.font_size == 14.0
    assert line.is_bold is True
    assert line.is_italic is False
    assert line.line_index == 0