import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def calculate_rank(row):
    if row['status'] == "정답" and row['elapsed_time'] < 30:
        return 1  # 시간이 짧게 걸린 정답
    elif row['status'] == "정답" and row['elapsed_time'] >= 30:
        return 2  # 시간이 오래 걸린 정답
    elif row['status'] != "정답" and row['elapsed_time'] < 30:
        return 3  # 시간이 짧게 걸린 오답
    elif row['status'] != "정답" and row['elapsed_time'] >= 30:
        return 4  # 시간이 오래 걸린 오답


def create_interaction_matrix(file_path):
    # records.csv 파일 읽기
    records_df = pd.read_csv(file_path)

    # 각 기록에 대해 rank 계산
    records_df['rank'] = records_df.apply(calculate_rank, axis=1)

    # 사용자-문제 상호작용 행렬 생성
    user_problem_matrix = records_df.pivot_table(
        index='student_id',
        columns='problem_id',
        values='rank',
        fill_value=0
    )

    return user_problem_matrix


def calculate_user_similarity(user_problem_matrix):
    """
    사용자 간 유사도를 계산합니다.

    Args:
    user_problem_matrix (DataFrame): 사용자-문제 상호작용 행렬

    Returns:
    DataFrame: 사용자 간의 유사도 행렬
    """
    # 코사인 유사도 계산
    user_similarity = cosine_similarity(user_problem_matrix)

    # 유사도 행렬을 데이터프레임으로 변환
    user_similarity_df = pd.DataFrame(user_similarity,
                                      index=user_problem_matrix.index,
                                      columns=user_problem_matrix.index)
    return user_similarity_df


def recommend_problems(user_similarity_matrix, user_problem_matrix, student_id, top_n=5, top_similar_users=5):
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
    if student_id not in user_similarity_matrix.index:
        return []

    # 사용자 유사도 행렬에서 유사도가 높은 순으로 정렬하고,
    # 자기자신을 제외하고 유사도 높은 순으로 5명만 잘라내기
    similar_users = (user_similarity_matrix[student_id].sort_values(ascending=False)
                     .drop(student_id).head(top_similar_users))

    similar_users = similar_users[:5]
    print(f"{student_id}번 사용자와 유사한 사용자 : {similar_users}")  # 로그

    recommended_problems = []
    user_solved_problems = user_problem_matrix.loc[student_id][user_problem_matrix.loc[student_id] > 0].index

    for similar_user in similar_users.index:
        # 특정 유사도가 높은 사용자가 푼 문제와 rank 점수를 가져옴.
        similar_user_problems = user_problem_matrix.loc[similar_user]

        # 유사 사용자가 푼 문제 중에서 현재 사용자가 아직 풀지 않은 문제를 필터링
        new_problems = similar_user_problems[similar_user_problems > 0].drop(user_solved_problems, errors='ignore')

        # 새로운 문제에서 가장 높은 점수를 받은 문제 하나 선택
        if not new_problems.empty:
            top_problem = new_problems.sort_values(ascending=False).index[0]
            recommended_problems.append((similar_user, top_problem))

        # 추천할 문제 수가 충분하면 종료
        if len(recommended_problems) >= top_n:
            break

    return recommended_problems

# 함수 실행
file_path = '../data/records.csv'

# 사용자-문제 상호작용 행렬 생성
user_problem_matrix = create_interaction_matrix(file_path)
# 사용자 간 유사도 계산
user_similarity_matrix = calculate_user_similarity(user_problem_matrix)
# 특정 사용자에게 문제 추천
recommended_problems = recommend_problems(user_similarity_matrix, user_problem_matrix, student_id=1, top_n=5)

###### 출력 확인 및 엑셀 다운로드 ######
# # 행렬 출력
# print(user_problem_matrix)
# user_problem_matrix.to_excel("../data/user_problem_matrix.xlsx")
#
# # 유사도 행렬 출력
# print(user_similarity_matrix)
#user_similarity_matrix.to_excel("../data/user_similarity_matrix.xlsx")
#
# # 추천 문제 ID 출력

print("추천 문제 (유사도가 높은 사용자 ID, 문제 ID)", recommended_problems)
