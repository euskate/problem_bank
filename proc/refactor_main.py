import pandas as pd
import random

# 문제 CSV 파일 경로
file_path = '../problems.csv'

# CSV 파일 읽기
df = pd.read_csv(file_path)


def select_random_problem(dataframe):
    """
    랜덤한 문제를 선택합니다.

    Args:
    dataframe (DataFrame): 문제 데이터가 포함된 DataFrame.

    Returns:
    Series: 랜덤하게 선택된 문제.
    """
    random_index = random.randint(0, len(dataframe) - 1)
    return dataframe.iloc[random_index]


def display_problem(problem):
    """
    문제의 제목과 설명을 출력합니다.

    Args:
    problem (Series): 선택된 문제.
    """
    print("\n" + "=" * 50 + "\n")
    title = problem['title']
    description = problem['description']
    topic = problem.get('topic', '일반')  # 'topic'이 없을 경우 '일반'으로 설정

    print(f"<{topic}> 문제: {title}\n")
    for line in description.split('\\n'):
        print(line.strip())
    print("\n" + "=" * 50 + "\n")


def get_user_input():
    """
    사용자로부터 답을 입력받습니다.

    Returns:
    str: 사용자가 입력한 답.
    """
    return input("답을 입력하세요(1, 2, 3, 4, q:종료): ").strip().lower()


def check_answer(problem, user_answer):
    """
    사용자의 답을 정답과 비교하고 피드백을 제공합니다.

    Args:
    problem (Series): 선택된 문제.
    user_answer (str): 사용자가 입력한 답.

    Returns:
    bool: 정답 여부.
    """
    correct_answer = str(problem['answer'])

    if user_answer == correct_answer:
        print("✅ 정답입니다! 잘 하셨어요! 🎉\n")
        return True
    else:
        print("❌ 오답입니다. 다음 기회에 다시 도전해보세요. 😢\n")
        return False


def show_solution(problem):
    """
    정답 및 해설을 출력합니다.

    Args:
    problem (Series): 선택된 문제.
    """
    print("\n" + "=" * 50 + "\n")
    correct_answer = problem['answer']
    solution = problem.get('solution', "해설이 제공되지 않았습니다.")
    print(f"🔍 정답: {correct_answer}")
    print(f"💡 해설: {solution}\n")

def main():
    """
    메인 실행 함수. 사용자에게 문제를 제시하고 답을 입력받아 정답을 확인합니다.
    """
    while True:
        selected_problem = select_random_problem(df)
        display_problem(selected_problem)

        user_answer = get_user_input()

        if user_answer == 'q':
            print("👋 프로그램을 종료합니다. 학습을 마치신 것을 축하드립니다! 🎓")
            break

        if check_answer(selected_problem, user_answer):
            continue  # 정답을 맞췄으므로 다음 문제로
        else:
            if ask_for_solution():
                show_solution(selected_problem)


def ask_for_solution():
    """
    사용자가 정답과 해설을 확인할지 물어봅니다.

    Returns:
    bool: 사용자가 해설을 보기를 원하는지 여부.
    """
    while True:
        choice = input("🔍 정답과 해설을 확인하시겠습니까? (y/n): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            print("🔄 다음 문제로 넘어갑니다.\n")
            return False
        else:
            print("잘못된 입력입니다. 'y' 또는 'n'을 입력해주세요.")


if __name__ == "__main__":
    main()
