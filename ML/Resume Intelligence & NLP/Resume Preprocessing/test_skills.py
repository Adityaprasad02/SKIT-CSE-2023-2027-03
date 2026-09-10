from app.services.parser import extract_text
from app.services.preprocessor import preprocess_resume
from app.services.section_extractor import extract_sections
from app.services.skill_extractor import extract_skills


file_path = "sample_resume.pdf"

# Extract resume text
raw_text = extract_text(file_path)

# Preprocess text
cleaned_text = preprocess_resume(raw_text)

# Extract sections
sections = extract_sections(cleaned_text)

# Extract skills only from Skills section
skills_text = sections["skills"]

skills = extract_skills(skills_text)


print("\n========== EXTRACTED SKILLS ==========\n")

for category, skill_list in skills.items():

    print(f"\n--- {category.upper()} ---")

    if skill_list:
        for skill in skill_list:
            print(f"- {skill}")

    else:
        print("None")