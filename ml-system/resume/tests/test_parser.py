from parsing.parser import parse_resume

file_path = "tests/sample_resume.pdf"

text = parse_resume(file_path)

print(text)