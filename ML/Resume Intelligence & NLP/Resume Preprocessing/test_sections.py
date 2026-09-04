from app.services.parser import extract_text
from app.services.preprocessor import preprocess_resume
from app.services.section_extractor import extract_sections


file_path = "sample_resume.pdf"

# Extract
raw_text = extract_text(file_path)

# Preprocess
cleaned_text = preprocess_resume(raw_text)

# Extract sections
sections = extract_sections(cleaned_text)


print("\n========== RESUME SECTIONS ==========\n")

for section, content in sections.items():
    print(f"\n--- {section.upper()} ---\n")
    print(content)