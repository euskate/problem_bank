from data_loader import DataLoader
from quiz import Quiz
from auth import Auth

def main():
    """
    메인 실행 함수. 학생 로그인 및 퀴즈 시작을 처리합니다.
    """
    # Auth 인스턴스 생성
    auth = Auth('../students.csv')

    # 사용자 로그인 또는 회원가입
    print("📝 회원가입 / 로그인")
    while True:
        choice = input("1. 로그인\n2. 회원가입\n선택하세요 (1/2): ").strip()
        if choice == '1':
            email = input("이메일을 입력하세요: ").strip()
            student = auth.login(email)
            if student:
                break
        elif choice == '2':
            name = input("이름을 입력하세요: ").strip()
            email = input("이메일을 입력하세요: ").strip()
            student = auth.register(name, email)
            if student:
                break
        else:
            print("잘못된 선택입니다. 1 또는 2를 입력하세요.")

    # 로그인된 사용자 정보 출력
    current_user = auth.get_current_user()
    if current_user:
        print(f"현재 로그인된 사용자: {current_user.name} ({current_user.email})")

    # 문제 데이터 로드
    loader = DataLoader('../problems.csv')
    problems = loader.load_problems()

    # 퀴즈 시작
    if problems:
        quiz = Quiz(problems)
        quiz.start()
    else:
        print("⚠️ 문제를 불러올 수 없습니다. 프로그램을 종료합니다.")

if __name__ == "__main__":
    main()
