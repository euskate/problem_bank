import pandas as pd
from problem import Problem

class DataLoader:
    def __init__(self, file_path):
        """
        DataLoader 클래스 생성자.

        Args:
        file_path (str): CSV 파일 경로.
        """
        self.file_path = file_path

    def load_problems(self):
        """
        CSV 파일에서 문제를 로드하여 Problem 객체 리스트로 반환합니다.

        Returns:
        list of Problem: 문제 객체 리스트.
        """
        problems = []
        try:
            df = pd.read_csv(self.file_path)
            print("📁 데이터 로드 성공!")

            for _, row in df.iterrows():
                problem = Problem(
                    problem_id=row['problem_id'],
                    title=row['title'],
                    description=row['description'],
                    topic=row.get('topic', '일반'),
                    difficulty=row.get('difficulty', '보통'),
                    type=row.get('type', '객관식(4지선다)'),
                    answer=row['answer'],
                    solution=row.get('solution', "해설이 제공되지 않았습니다.")
                )
                problems.append(problem)
            return problems
        except FileNotFoundError:
            print("❌ 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        except Exception as e:
            print(f"❌ 데이터를 로드하는 중 오류가 발생했습니다: {e}")
        return problems
