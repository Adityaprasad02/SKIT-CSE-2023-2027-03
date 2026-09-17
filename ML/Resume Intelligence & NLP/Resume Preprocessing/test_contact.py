from app.services.parser import extract_text
from app.services.preprocessor import preprocess_resume
from app.services.contact_extractor import extract_contact_information


file_path = "sample_resume.pdf"

# Extract text
raw_text = extract_text(file_path)

# Preprocess text
cleaned_text = preprocess_resume(raw_text)

# Extract contact information
contact = extract_contact_information(cleaned_text)


print("\n========== CONTACT INFORMATION ==========\n")

for key, value in contact.items():
    print(f"{key}: {value}")