class Problem:
    def __init__(self, problem_id, title, description, topic, difficulty, type, answer, solution):
        """
        Problem 클래스 생성자.

        Args:
        problem_id (int): 문제 ID.
        title (str): 문제 제목.
        description (str): 문제 설명.
        topic (str): 문제 주제.
        difficulty (str): 문제 난이도 ('어려움', '보통', '쉬움').
        type (str): 문제 유형 ('객관식(4지선다)', '주관식').
        answer (str): 문제 정답.
        solution (str): 정답 해설.
        """
        self.problem_id = problem_id
        self.title = title
        self.description = description
        self.topic = topic
        self.difficulty = difficulty
        self.type = type
        self.answer = str(answer)  # 정답은 문자열로 저장
        self.solution = solution

    def display(self):
        """
        문제의 제목과 설명을 출력합니다.
        """
        print("\n" + "=" * 50 + "\n")
        print(f"[ID: {self.problem_id}] <{self.topic}> 문제: {self.title} (난이도: {self.difficulty})\n")
        for line in self.description.split('\\n'):
            print(line.strip())
        print("\n" + "=" * 50 + "\n")

    def check_answer(self, user_answer):
        """
        사용자 입력과 정답을 비교합니다.

        Args:
        user_answer (str): 사용자가 입력한 답.

        Returns:
        bool: 정답 여부.
        """
        if user_answer == self.answer:
            print("✅ 정답입니다! 잘 하셨어요! 🎉\n")
            return True
        else:
            print("❌ 오답입니다. 다음 기회에 다시 도전해보세요. 😢\n")
            return False

    def show_solution(self):
        """
        정답 및 해설을 출력합니다.
        """
        print("\n" + "=" * 50 + "\n")
        print(f"🔍 정답: {self.answer}")
        print(f"💡 해설: {self.solution}\n")
        print("\n" + "=" * 50 + "\n")
