def get_student_profile(student_name: str):
    # In future → fetch from DB
    # For now → static sample

    return {
        "education": [
            {
                "degree": "B.Tech Computer Science",
                "institution": "XYZ Institute of Technology",
                "year": "2025"
            }
        ],
        "certifications": [
            {
                "title": "Python Programming Certification",
                "provider": "Coursera",
                "year": "2024"
            },
            {
                "title": "SQL Fundamentals",
                "provider": "HackerRank",
                "year": "2023"
            }
        ],
        "work_experience": [
            {
                "company": "ABC Tech Solutions",
                "role": "Backend Intern",
                "description": "Worked on REST API development and database queries"
            }
        ]
    }
