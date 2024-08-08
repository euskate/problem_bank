import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationSystem:
    def __init__(self, records_file):
        self.records_file = records_file
        self.reload()

    def create_interaction_matrix(self):
        # records.csv 파일 읽기
        records_df = pd.read_csv(self.records_file)

        # 각 기록에 대해 rank 계산
        records_df['rank'] = records_df.apply(self.calculate_rank, axis=1)

        # 사용자-문제 상호작용 행렬 생성 (결측치는 0으로 채움)
        user_problem_matrix = records_df.pivot_table(
            index='student_id',
            columns='problem_id',
            values='rank',
            fill_value=0
        )

        return user_problem_matrix

    def calculate_rank(self, row):
        if row['status'] == "정답" and row['elapsed_time'] < 30:
            return 1  # 시간이 짧게 걸린 정답
        elif row['status'] == "정답" and row['elapsed_time'] >= 30:
            return 2  # 시간이 오래 걸린 정답
        elif row['status'] != "정답" and row['elapsed_time'] < 30:
            return 3  # 시간이 짧게 걸린 오답
        elif row['status'] != "정답" and row['elapsed_time'] >= 30:
            return 4  # 시간이 오래 걸린 오답

    def calculate_user_similarity(self):
        """
        사용자 간 유사도를 계산합니다.
        """
        # 코사인 유사도 계산
        user_similarity = cosine_similarity(self.user_problem_matrix)

        # 유사도 행렬을 데이터프레임으로 변환
        user_similarity_df = pd.DataFrame(user_similarity,
                                          index=self.user_problem_matrix.index,
                                          columns=self.user_problem_matrix.index)
        return user_similarity_df

    def recommend_problems(self, student_id, top_n=5, top_similar_users=5):
        """
        사용자에게 문제를 추천합니다.

        Args:
        user_similarity_matrix (DataFrame): 사용자 간 유사도 행렬
        user_problem_matrix (DataFrame): 사용자-문제 상호작용 행렬
        student_id (int): 추천할 사용자 ID
        top_n (int): 추천할 문제 개수
        top_similar_users (int): 유사도가 높은 사용자 수

        Returns:
        list of tuple: (추천 사용자 ID, 문제 ID) 리스트
        """
        if student_id not in self.user_similarity_matrix.index:
            return []

        # 유사한 사용자 중 상위 top_similar_users 찾기
        similar_users = self.user_similarity_matrix[student_id].sort_values(ascending=False).drop(student_id).head(
            top_similar_users)
        print(f"{student_id}번 사용자와 유사한 사용자 : {similar_users}")  # 로그

        recommended_problems = []
        user_solved_problems = self.user_problem_matrix.loc[student_id][
            self.user_problem_matrix.loc[student_id] > 0].index

        for similar_user in similar_users.index:
            similar_user_problems = self.user_problem_matrix.loc[similar_user]
            # 새로운 문제 필터링
            new_problems = similar_user_problems[similar_user_problems > 0].drop(user_solved_problems, errors='ignore')

            # 새로운 문제에서 가장 높은 점수를 받은 문제 하나 선택
            if not new_problems.empty:
                top_problem = new_problems.sort_values(ascending=False).index[0]
                recommended_problems.append((similar_user, top_problem))

            # 추천할 문제 수가 충분하면 종료
            if len(recommended_problems) >= top_n:
                break

        return recommended_problems

    def reload(self):
        self.user_problem_matrix = self.create_interaction_matrix()
        self.user_similarity_matrix = self.calculate_user_similarity()