import random
from utils import get_user_input, ask_for_solution

class Quiz:
    def __init__(self, problems):
        """
        Quiz 클래스 생성자.

        Args:
        problems (list of Problem): 문제 객체 리스트.
        """
        self.problems = problems

    def start(self):
        """
        퀴즈를 시작합니다.
        """
        while True:
            problem = self.get_random_problem()
            problem.display()

            user_answer = get_user_input()

            if user_answer == 'q':
                print("👋 프로그램을 종료합니다. 학습을 마치신 것을 축하드립니다! 🎓")
                break

            if problem.check_answer(user_answer):
                continue  # 정답을 맞췄으므로 다음 문제로
            else:
                if ask_for_solution():
                    problem.show_solution()

    def get_random_problem(self):
        """
        랜덤한 문제를 반환합니다.

        Returns:
        Problem: 랜덤하게 선택된 문제.
        """
        return random.choice(self.problems)
