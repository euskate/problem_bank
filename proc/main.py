import pandas as pd
import random

# 문제 CSV 파일 경로
file_path = '../problems.csv'

# CSV 파일 읽기
df = pd.read_csv(file_path)


# 랜덤한 문제 선택
def select_random_problem(dataframe):
    random_index = random.randint(0, len(dataframe) - 1)
    random_problem = dataframe.iloc[random_index]
    return random_problem


# 문제의 제목과 설명을 출력하는 함수
def display_problem(problem):
    print("\n" + "=" * 50 + "\n")
    # 제목과 설명을 변수에 저장
    title = problem['title']
    description = problem['description']

    # 제목 출력
    print(f"<{problem['topic']}> 문제: {title}\n  ")

    # 설명 출력 - \n을 기준으로 줄을 나눔
    for line in description.split('\\n'):  # \\n을 기준으로 줄 나누기
        print(line.strip())

    print("\n" + "=" * 50 + "\n")


# 사용자 입력을 받는 함수
def get_user_input():
    user_input = input("답을 입력하세요(1, 2, 3, 4, q:종료): ")
    return user_input


# 정답을 비교하고 피드백을 제공하는 함수
def check_answer(problem, user_answer):
    correct_answer = str(problem['answer'])  # 정답을 문자열로 변환

    if user_answer.strip() == correct_answer.strip():
        print("✅ 정답입니다! 잘 하셨어요! 🎉\n")
        return True
    else:
        print("❌ 오답입니다. 다음 기회에 다시 도전해보세요. 😢\n")
        return False


# 정답 및 해설을 보여주는 함수
def show_solution(problem):
    print("\n" + "=" * 50 + "\n")
    correct_answer = problem['answer']
    solution = problem['solution'] if 'solution' in problem else "해설이 제공되지 않았습니다."
    print(f"🔍 정답: {correct_answer}")
    print(f"💡 해설: {solution}\n")
    print("\n" + "=" * 50 + "\n")


# 메인 실행 함수
def main():
    while True:  # 무한 루프 시작
        # 랜덤 문제 선택
        selected_problem = select_random_problem(df)

        # 문제 출력
        display_problem(selected_problem)

        # 사용자 답안 입력
        user_answer = get_user_input()

        if user_answer.lower() == 'q':
            print("👋 프로그램을 종료합니다. 학습을 마치신 것을 축하드립니다! 🎓")
            return

        # 정답 확인 및 피드백
        if check_answer(selected_problem, user_answer):
            pass
        else:
            # 오답일 경우 정답 및 해설을 확인할 것인지 묻기
            see_solution = input("정답과 해설을 확인하시겠습니까? (y/n): ")
            if see_solution.lower() == 'y':
                show_solution(selected_problem)
            else:
                print("🔄 다음 문제로 넘어갑니다.\n")
                pass


if __name__ == "__main__":
    main()
