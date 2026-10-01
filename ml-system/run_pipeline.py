from pathlib import Path

from resume.parsing.parser import parse_resume_structured
from resume.preprocessing.line_segmenter import segment_lines
from resume.preprocessing.header_detector import detect_headers
from resume.preprocessing.section_segmenter import segment_sections
from resume.preprocessing.contact_extractor import extract_contact_info


RESUME_PATH = Path(
    "resume/tests/integration/fixtures/sample_resume.docx"
)


def main():

    print("\n" + "=" * 70)
    print("STEP 1: PARSING RESUME")
    print("=" * 70)

    raw_lines = parse_resume_structured(str(RESUME_PATH))

    print(f"\nTotal Raw Lines: {len(raw_lines)}\n")

    for line in raw_lines:
        print(
            f"[{line.line_index}] "
            f"Text: {line.text}"
        )


    print("\n" + "=" * 70)
    print("STEP 2: PREPROCESSING - LINE SEGMENTATION")
    print("=" * 70)

    lines = segment_lines(raw_lines)

    print(f"\nTotal Processed Lines: {len(lines)}\n")

    for line in lines:
        print(
            f"[{line.line_index}] "
            f"{line.text}"
        )


    print("\n" + "=" * 70)
    print("STEP 3: HEADER DETECTION")
    print("=" * 70)

    header_candidates = detect_headers(lines)

    for candidate in header_candidates:
        print(
            f"Header: {candidate.line.text}"
        )
        print(
            f"Score: {candidate.score}"
        )
        print()


    print("\n" + "=" * 70)
    print("STEP 4: SECTION SEGMENTATION")
    print("=" * 70)

    segmented = segment_sections(
        lines,
        header_candidates
    )

    for section_name, section_lines in segmented.sections.items():

        print(f"\n[{section_name.upper()}]")

        for line in section_lines:
            print(line)


    print("\n" + "=" * 70)
    print("STEP 5: CONTACT EXTRACTION")
    print("=" * 70)

    full_text = "\n".join(
        line.text
        for line in sorted(
            lines,
            key=lambda line: line.line_index
        )
    )

    contact_info = extract_contact_info(full_text)

    print("\nEmails:")
    print(contact_info.emails)

    print("\nPhones:")
    print(contact_info.phones)

    print("\nLinkedIn:")
    print(contact_info.linkedin)

    print("\nGitHub:")
    print(contact_info.github)


if __name__ == "__main__":
    main()