"""
Academic Reporting, Class Analytics, and Rank Calculator.
"""
from typing import List, Dict, Any
from models.student import Student
from config import GRADE_SCALE, MIN_ATTENDANCE_PERCENT

class ReportManager:
    def __init__(self, students: List[Student]):
        self.students = students

    def get_toppers(self, count: int = 3) -> List[Student]:
        graded = [s for s in self.students if s.marks]
        return sorted(graded, key=lambda s: s.percentage, reverse=True)[:count]

    def get_student_rank(self, student_id: str) -> int:
        graded = sorted([s for s in self.students if s.marks], key=lambda s: s.percentage, reverse=True)
        for idx, s in enumerate(graded):
            if s.student_id.upper() == student_id.upper():
                return idx + 1
        return 0

    def generate_pass_fail_summary(self) -> Dict[str, Any]:
        total = len(self.students)
        if total == 0:
            return {"total": 0, "passed": 0, "failed": 0, "pass_pct": 0.0, "fail_pct": 0.0}
        passed = sum(1 for s in self.students if s.is_passed)
        failed = total - passed
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_pct": round((passed / total) * 100, 2),
            "fail_pct": round((failed / total) * 100, 2)
        }

    def generate_grade_distribution(self) -> Dict[str, int]:
        dist = {grade: 0 for _, grade in GRADE_SCALE}
        for s in self.students:
            if s.marks and s.grade in dist:
                dist[s.grade] += 1
        return dist

    def generate_attendance_summary(self) -> Dict[str, Any]:
        if not self.students:
            return {"avg_att": 0.0, "highest": 0.0, "lowest": 0.0, "shortage_count": 0}
        rates = [s.attendance_percentage for s in self.students]
        shortage = sum(1 for r in rates if r < MIN_ATTENDANCE_PERCENT)
        return {
            "avg_att": round(sum(rates) / len(rates), 2),
            "highest": max(rates),
            "lowest": min(rates),
            "shortage_count": shortage
        }

    def generate_subject_wise_analysis(self) -> Dict[str, Dict[str, float]]:
        subject_scores: Dict[str, list[float]] = {}
        for s in self.students:
            for sub, score in s.marks.items():
                subject_scores.setdefault(sub, []).append(score)

        summary = {}
        for sub, scores in subject_scores.items():
            if scores:
                summary[sub] = {
                    "avg": round(sum(scores) / len(scores), 2),
                    "highest": max(scores),
                    "lowest": min(scores)
                }
        return summary

    def get_class_performance_summary(self) -> Dict[str, Any]:
        total = len(self.students)
        if total == 0:
            return {}
        percentages = [s.percentage for s in self.students if s.marks]
        toppers = self.get_toppers(1)
        topper_name = f"{toppers[0].name} ({toppers[0].percentage}%)" if toppers else "N/A"

        return {
            "total_students": total,
            "average_percentage": round(sum(percentages) / len(percentages), 2) if percentages else 0.0,
            "highest_percentage": max(percentages) if percentages else 0.0,
            "lowest_percentage": min(percentages) if percentages else 0.0,
            "topper": topper_name,
            "pass_fail": self.generate_pass_fail_summary(),
            "grade_distribution": self.generate_grade_distribution(),
            "attendance": self.generate_attendance_summary()
        }