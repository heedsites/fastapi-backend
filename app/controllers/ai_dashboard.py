from app.services.question_analyzer import QuestionAnalyzer
from app.database import question_analysis_collection
from app.services.query_interpreter import QueryInterpreter

analyzer = QuestionAnalyzer()
query_interpreter = QueryInterpreter()


def analyze_question_controller(question: str):
    """
    Analyze and store question classification
    """

    # check if already analyzed
    existing = question_analysis_collection.find_one({"question": question})
    if existing:
        return {
            "domain": existing["domain"],
            "concept": existing["concept"],
            "difficulty": existing["difficulty"]
        }

    # analyze using AI
    result = analyzer.classify_question(question)

    # store in DB
    question_analysis_collection.insert_one({
        "question": question,
        "domain": result["domain"],
        "concept": result["concept"],
        "difficulty": result["difficulty"]
    })

    return result
from app.services.performance_analyzer import PerformanceAnalyzer

performance_analyzer = PerformanceAnalyzer()


def top_performers_controller(submissions, top_n: int):
    submissions_dict = [s.dict() for s in submissions]
    result = performance_analyzer.get_top_performers(submissions_dict, top_n)
    return result
from app.services.insight_generator import InsightGenerator

insight_generator = InsightGenerator()

def ensure_questions_classified(submissions):
    """
    Automatically classify questions if not already stored
    """
    for s in submissions:
        existing = question_analysis_collection.find_one({"question": s.dict()["question"]})
        if not existing:
            analyze_question_controller(s.dict()["question"])

def top_performers_with_summary(submissions, top_n: int):
    ranked = performance_analyzer.get_top_performers(
        [s.dict() for s in submissions], top_n
    )

    for student in ranked:
        summary = insight_generator.generate_student_summary(student)
        student["summary"] = summary

    return ranked
def batch_insight_controller(submissions):
    submissions_dict = [s.dict() for s in submissions]

    batch_data = performance_analyzer.analyze_batch_performance(submissions_dict)

    summary = insight_generator.generate_batch_summary(batch_data)

    return {
        "analytics": batch_data,
        "summary": summary
    }
def query_dashboard_controller(question: str, submissions):
    """
    Main AI dashboard entry point.
    Interprets faculty question and routes to correct analytics engine.
    """

    parsed = query_interpreter.interpret(question)

    intent = parsed.get("intent")
    limit = parsed.get("limit", 10)

    submissions_dict = [s.dict() for s in submissions]
    ensure_questions_classified(submissions)

    if intent == "top_performers":
        ranked = performance_analyzer.get_top_performers(submissions_dict, limit)

        for student in ranked:
            student["summary"] = insight_generator.generate_student_summary(student)

        return {
            "type": "top_performers",
            "message":"Top performing students based on overall concept mastery",
            "data": ranked
        }

    elif intent == "batch_insight":
        batch_data = performance_analyzer.analyze_batch_performance(submissions_dict)
        summary = insight_generator.generate_batch_summary(batch_data)

        return {
            "type": "batch_insight",
            "message":"Overall batch performance analysis",
            "analytics": batch_data,
            "summary": summary
        }

    else:
        return {"message": "Unable to understand the query"}
