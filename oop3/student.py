class Student:
    def __init__(self, student_id, name, email):
        """
        Student 클래스 생성자.

        Args:
        student_id (int): 학생 ID.
        name (str): 학생 이름.
        email (str): 학생 이메일.
        """
        self.student_id = student_id
        self.name = name
        self.email = email

    def display_info(self):
        """
        학생 정보를 출력합니다.
        """
        print(f"학생 ID: {self.student_id}")
        print(f"이름: {self.name}")
        print(f"이메일: {self.email}")
