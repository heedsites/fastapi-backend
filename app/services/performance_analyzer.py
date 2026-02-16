from collections import defaultdict
from app.database import question_analysis_collection


class PerformanceAnalyzer:

    def build_student_profiles(self, submissions: list):
        """
        submissions: list of student answer records
        returns: student skill profiles
        """

        # student -> concept -> [correct, total]
        student_concept_stats = defaultdict(lambda: defaultdict(lambda: [0, 0]))

        for record in submissions:
            question_text = record["question"]
            student_id = record["student_id"]
            is_correct = record["is_correct"]

            # get concept from stored classification
            analysis = question_analysis_collection.find_one({"question": question_text})
            if not analysis:
                continue  # skip unclassified questions

            concept = analysis["concept"]

            student_concept_stats[student_id][concept][1] += 1  # total
            if is_correct:
                student_concept_stats[student_id][concept][0] += 1  # correct

        # convert to percentage profile
        student_profiles = {}

        for student, concepts in student_concept_stats.items():
            profile = {}
            for concept, (correct, total) in concepts.items():
                profile[concept] = round((correct / total) * 100, 2) if total else 0

            student_profiles[student] = profile

        return student_profiles
    def get_top_performers(self, submissions: list, top_n: int = 10):
        """
        Returns top N students based on overall concept accuracy
        """

        profiles = self.build_student_profiles(submissions)

        student_scores = []

        for student, concepts in profiles.items():
            if not concepts:
                continue

            overall = sum(concepts.values()) / len(concepts)

            student_scores.append({
                "student_id": student,
                "overall_score": round(overall, 2),
                "concept_breakdown": concepts
            })

        # sort descending
        ranked = sorted(student_scores, key=lambda x: x["overall_score"], reverse=True)

        return ranked[:top_n]
    def analyze_batch_performance(self, submissions: list):
        """
        Aggregate performance across entire batch
        """

        student_profiles = self.build_student_profiles(submissions)

        concept_totals = {}
        concept_counts = {}

        # aggregate all students
        for profile in student_profiles.values():
            for concept, score in profile.items():
                concept_totals[concept] = concept_totals.get(concept, 0) + score
                concept_counts[concept] = concept_counts.get(concept, 0) + 1

        # compute averages
        avg_scores = {}
        for concept in concept_totals:
            avg_scores[concept] = round(concept_totals[concept] / concept_counts[concept], 2)

        # determine strong & weak
        strong_topics = [c for c, s in avg_scores.items() if s >= 70]
        weak_topics = [c for c, s in avg_scores.items() if s <= 40]

        return {
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "average_scores": avg_scores
        }
