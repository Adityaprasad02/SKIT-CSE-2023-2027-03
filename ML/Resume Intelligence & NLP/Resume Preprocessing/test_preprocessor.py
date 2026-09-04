from app.services.parser import extract_text
from app.services.preprocessor import preprocess_resume


file_path = "sample_resume.pdf"

# Step 1: Extract text
raw_text = extract_text(file_path)

# Step 2: Preprocess text
cleaned_text = preprocess_resume(raw_text)

print("\n========== RAW RESUME TEXT ==========\n")
print(raw_text)

print("\n========== CLEANED RESUME TEXT ==========\n")
print(cleaned_text)