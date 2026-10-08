"""
Canonical skill definitions used by the resume
and job-description matching system.

Each canonical skill has a collection of common
ways in which that skill may appear in text.
"""

"""
Skill vocabulary used by the Resume Intelligence system.

The dictionary maps common skill names and aliases to a
canonical skill name.

This is intentionally separated from the extraction logic
so the vocabulary can be expanded independently.
"""


SKILL_ALIASES = {

    # --------------------------------------------------
    # Programming Languages
    # --------------------------------------------------

    "python": {
        "python",
        "python3",
    },

    "java": {
        "java",
        "core java",
        "java 8",
        "java 11",
        "java 17",
        "java 21",
    },

    "c": {
        "c",
        "c language",
    },

    "c++": {
        "c++",
        "cpp",
    },

    "c#": {
        "c#",
        "c sharp",
    },

    "javascript": {
        "javascript",
    },

    "typescript": {
        "typescript",
        "ts",
    },

    "go": {
        "golang",
        "go language",
    },

    "rust": {
        "rust",
    },

    "kotlin": {
        "kotlin",
    },

    "swift": {
        "swift",
    },


    # --------------------------------------------------
    # Frontend
    # --------------------------------------------------

    "html": {
        "html",
        "html5",
    },

    "css": {
        "css",
        "css3",
    },

    "react": {
        "react",
        "reactjs",
        "react.js",
    },

    "angular": {
        "angular",
        "angularjs",
    },

    "vue.js": {
        "vue",
        "vuejs",
        "vue.js",
    },

    "next.js": {
        "nextjs",
        "next.js",
    },

    "tailwind css": {
        "tailwind",
        "tailwind css",
        "tailwindcss",
    },

    "bootstrap": {
        "bootstrap",
    },


    # --------------------------------------------------
    # Backend / Frameworks
    # --------------------------------------------------

    "node.js": {
        "node",
        "nodejs",
        "node.js",
    },

    "express.js": {
        "express",
        "expressjs",
        "express.js",
    },

    "spring": {
        "spring framework",
        "spring",
    },

    "spring boot": {
        "spring boot",
        "springboot",
    },

    "django": {
        "django",
    },

    "flask": {
        "flask",
    },

    "fastapi": {
        "fastapi",
        "fast api",
    },


    # --------------------------------------------------
    # Databases
    # --------------------------------------------------

    "sql": {
        "sql",
    },

    "mysql": {
        "mysql",
    },

    "postgresql": {
        "postgresql",
        "postgres",
        "postgre sql",
    },

    "mongodb": {
        "mongodb",
        "mongo db",
        "mongo",
    },

    "redis": {
        "redis",
    },

    "oracle database": {
        "oracle database",
        "oracle db",
        "oracle",
    },

    "sqlite": {
        "sqlite",
    },


    # --------------------------------------------------
    # APIs / Architecture
    # --------------------------------------------------

    "rest api": {
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
    },

    "graphql": {
        "graphql",
    },

    "microservices": {
        "microservices",
        "microservice architecture",
    },

    "web services": {
        "web services",
        "web service",
    },


    # --------------------------------------------------
    # DevOps / Cloud
    # --------------------------------------------------

    "git": {
        "git",
    },

    "github": {
        "github",
    },

    "gitlab": {
        "gitlab",
    },

    "docker": {
        "docker",
        "docker container",
    },

    "kubernetes": {
        "kubernetes",
        "k8s",
    },

    "jenkins": {
        "jenkins",
    },

    "ci/cd": {
        "ci/cd",
        "ci cd",
        "continuous integration",
        "continuous delivery",
        "continuous deployment",
    },

    "aws": {
        "aws",
        "amazon web services",
    },

    "microsoft azure": {
        "azure",
        "microsoft azure",
    },

    "google cloud": {
        "google cloud",
        "gcp",
        "google cloud platform",
    },


    # --------------------------------------------------
    # Data Science / Machine Learning
    # --------------------------------------------------

    "machine learning": {
        "machine learning",
        "ml",
    },

    "deep learning": {
        "deep learning",
        "dl",
    },

    "artificial intelligence": {
        "artificial intelligence",
        "ai",
    },

    "data science": {
        "data science",
    },

    "data analysis": {
        "data analysis",
        "data analytics",
    },

    "natural language processing": {
        "natural language processing",
        "nlp",
    },

    "computer vision": {
        "computer vision",
        "cv",
    },

    "tensorflow": {
        "tensorflow",
    },

    "pytorch": {
        "pytorch",
        "torch",
    },

    "scikit-learn": {
        "scikit-learn",
        "sklearn",
    },

    "pandas": {
        "pandas",
    },

    "numpy": {
        "numpy",
    },

    "opencv": {
        "opencv",
        "opencv-python",
    },

    "xgboost": {
        "xgboost",
    },

    "lightgbm": {
        "lightgbm",
    },

    "catboost": {
        "catboost",
    },

    "streamlit": {
        "streamlit",
    },


    # --------------------------------------------------
    # Core Computer Science
    # --------------------------------------------------

    "data structures": {
        "data structures",
        "data structure",
        "dsa",
    },

    "algorithms": {
        "algorithms",
        "algorithm",
    },

    "object oriented programming": {
        "oop",
        "object oriented programming",
        "object-oriented programming",
    },

    "operating systems": {
        "operating systems",
        "operating system",
        "os",
    },

    "computer networks": {
        "computer networks",
        "computer network",
    },

    "database management systems": {
        "database management systems",
        "dbms",
    },

    "computer architecture": {
        "computer architecture",
        "computer organization",
        "coa",
    },


    # --------------------------------------------------
    # Testing / Development Practices
    # --------------------------------------------------

    "unit testing": {
        "unit testing",
        "unit test",
        "unit tests",
    },

    "pytest": {
        "pytest",
    },

    "junit": {
        "junit",
    },

    "agile": {
        "agile",
        "agile methodology",
    },

    "scrum": {
        "scrum",
    },
}
RELATED_SKILLS = {
    "sql": {
        "mysql",
        "postgresql",
        "oracle database",
        "sqlite",
    },
    "javascript": {
        "typescript",
    },
    "machine learning": {
        "scikit-learn",
        "xgboost",
        "lightgbm",
        "catboost",
    },
    "deep learning": {
        "pytorch",
        "tensorflow",
    },
    "artificial intelligence": {
        "machine learning",
        "deep learning",
    },
    "data science": {
        "data analysis",
        "machine learning",
        "pandas",
        "numpy",
    },
    "computer vision": {
        "opencv",
        "deep learning",
    },
}