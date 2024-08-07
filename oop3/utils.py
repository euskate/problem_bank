def get_user_input():
    """
    사용자로부터 답을 입력받습니다.

    Returns:
    str: 사용자가 입력한 답.
    """
    return input("답을 입력하세요(1, 2, 3, 4, q:종료): ").strip().lower()

def ask_for_solution():
    """
    사용자가 정답과 해설을 확인할지 물어봅니다.

    Returns:
    bool: 사용자가 해설을 보기를 원하는지 여부.
    """
    while True:
        choice = input("정답과 해설을 확인하시겠습니까? (y/n): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            print("🔄 다음 문제로 넘어갑니다.\n")
            return False
        else:
            print("잘못된 입력입니다. 'y' 또는 'n'을 입력해주세요.")
