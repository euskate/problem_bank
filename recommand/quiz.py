import random
import time
from flask import flash

from problem import Problem
from record_manager import RecordManager
from student import Student


class Quiz:
    def __init__(self, problems, student: Student, record_manager: RecordManager):
        """
        Quiz 클래스 생성자.

        Args:
        problems (list of Problem): 문제 객체 리스트.
        student (Student): 현재 로그인한 학생 객체.
        record_manager (RecordManager): 기록 관리 객체.
        """
        self.problems = problems
        self.student = student
        self.record_manager = record_manager
        self.current_problem = None
        self.start_time = 0  # 시작 시간 초기화

    def get_random_problem(self):
        """
        랜덤한 문제를 반환합니다.

        Returns:
        Problem: 랜덤하게 선택된 문제.
        """
        self.current_problem = random.choice(self.problems)
        self.start_time = time.time()  # 문제 시작 시간 기록
        # print(f"문제 시작 시간: {self.start_time}")  # 디버깅용
        return self.current_problem

    def get_problem_by_id(self, problem_id):
        """
        문제 ID를 기반으로 특정 문제를 반환합니다.

        Args:
        problem_id (int): 문제 ID.

        Returns:
        Problem: 특정 문제 ID에 해당하는 문제 또는 None.
        """
        problem = next((p for p in self.problems if p.problem_id == problem_id), None)
        if problem:
            self.current_problem = problem
            self.start_time = time.time()  # 문제 시작 시간 기록
            print(f"문제 시작 시간: {self.start_time}")  # 디버깅용
        return problem

    def submit_answer(self, problem_id, user_answer):
        """
        사용자의 답변을 제출하고 기록합니다.

        Args:
        problem_id (int): 문제 ID.
        user_answer (str): 사용자의 답변.
        """
        problem = next((p for p in self.problems if p.problem_id == problem_id), None)
        if not problem:
            flash("문제를 찾을 수 없습니다.", "danger")
            return

        end_time = time.time()  # 문제 종료 시간 기록
        print(f"문제 종료 시간: {end_time}")  # 디버깅용
        print(f"경과 시간: {end_time - self.start_time} 초")  # 디버깅용
        print(f"startTime: {self.start_time}")
        elapsed_time = int(end_time - self.start_time)  # 경과 시간 계산 (초 단위)

        is_correct = problem.check_answer(user_answer)

        score = 1 if is_correct else 0
        status = "정답" if is_correct else "오답"

        self.record_manager.add_record(
            student_id=self.student.student_id,
            problem_id=problem.problem_id,
            elapsed_time=elapsed_time,
            score=score,
            status=status,
            attempt_count=1  # 시도 횟수는 일단 1로 설정
        )

        if is_correct:
            flash("✅ 정답입니다! 잘 하셨어요! 🎉", "success")
        else:
            solution_message = f"❌ 오답입니다.<br>정답은 '{problem.answer}'입니다.<br>해설: {problem.solution}"
            flash(solution_message, "danger")
