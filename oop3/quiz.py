import random
import time
from utils import get_user_input, ask_for_solution
from record_manager import RecordManager

class Quiz:
    def __init__(self, problems, student, record_manager):
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

    def start(self):
        """
        퀴즈를 시작합니다.
        """
        while True:
            problem = self.get_random_problem()
            problem.display()

            start_time = time.time()  # 시작 시간 기록

            user_answer = get_user_input()

            if user_answer == 'q':
                print("👋 프로그램을 종료합니다. 학습을 마치신 것을 축하드립니다! 🎓")
                break

            attempt_count = 1
            elapsed_time = int(time.time() - start_time)  # 소요 시간 계산

            if problem.check_answer(user_answer):
                score = 1  # 정답 시 점수 1점
                status = "정답"
            else:
                score = 0
                status = "오답"
                if ask_for_solution():
                    problem.show_solution()


            # 기록 추가
            self.record_manager.add_record(
                student_id=self.student.student_id,
                problem_id=problem.problem_id,
                elapsed_time=elapsed_time,
                score=score,
                status=status,
                attempt_count=attempt_count
            )

    def get_random_problem(self):
        """
        랜덤한 문제를 반환합니다.

        Returns:
        Problem: 랜덤하게 선택된 문제.
        """
        return random.choice(self.problems)
