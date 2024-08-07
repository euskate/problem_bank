from data_loader import DataLoader
from quiz import Quiz

def main():
    """
    메인 실행 함수. 데이터를 로드하고 퀴즈를 시작합니다.
    """
    loader = DataLoader('../problems.csv')
    problems = loader.load_problems()

    if problems:
        quiz = Quiz(problems)
        quiz.start()
    else:
        print("⚠️ 문제를 불러올 수 없습니다. 프로그램을 종료합니다.")

if __name__ == "__main__":
    main()
