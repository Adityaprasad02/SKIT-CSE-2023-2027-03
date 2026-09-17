from app.services.semantic_analyzer import SemanticAnalyzer


resume_text = """
Software Engineer with experience in Android development.
Developed applications using Java, Kotlin, MVVM, Retrofit,
Coroutines and REST APIs.
"""


job_description = """
We are looking for an Android Developer with experience
in Kotlin, Java, MVVM, REST APIs and mobile application
development.
"""


analyzer = SemanticAnalyzer()

score = analyzer.calculate_similarity(
    resume_text,
    job_description
)


print("\n========== SEMANTIC ANALYSIS ==========\n")
print(f"Similarity Score: {score}")
print(f"Similarity Percentage: {score * 100:.2f}%")