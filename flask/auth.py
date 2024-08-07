import pandas as pd
from student import Student

class Auth:
    def __init__(self, file_path):
        """
        Auth 클래스 생성자.

        Args:
        file_path (str): 학생 데이터 CSV 파일 경로.
        """
        self.file_path = file_path
        self.students = self.load_students()
        self.current_user = None  # 현재 로그인한 사용자 정보

    def load_students(self):
        """
        CSV 파일에서 학생 데이터를 로드하여 Student 객체 리스트로 반환합니다.

        Returns:
        list of Student: 학생 객체 리스트.
        """
        students = []
        try:
            df = pd.read_csv(self.file_path)
            for _, row in df.iterrows():
                student = Student(
                    student_id=row['student_id'],
                    name=row['name'],
                    email=row['email']
                )
                students.append(student)
            return students
        except FileNotFoundError:
            print("❌ 학생 데이터 파일을 찾을 수 없습니다.")
        except Exception as e:
            print(f"❌ 학생 데이터를 로드하는 중 오류가 발생했습니다: {e}")
        return students

    def register(self, name, email):
        """
        학생을 등록합니다.

        Args:
        name (str): 학생 이름.
        email (str): 학생 이메일.

        Returns:
        Student: 등록된 학생 객체.
        """
        # 중복 이메일 검사
        if any(student.email == email for student in self.students):
            print("⚠️ 이미 존재하는 이메일입니다. 다른 이메일을 사용하세요.")
            return None

        # 새로운 학생 ID 생성
        new_id = max(student.student_id for student in self.students) + 1 if self.students else 1

        # 새로운 학생 등록
        new_student = Student(student_id=new_id, name=name, email=email)
        self.students.append(new_student)

        # 학생 데이터를 CSV 파일에 저장
        self.save_student(new_student)

        self.current_user = new_student  # 현재 사용자 설정

        print(f"✅ {name}님, 회원가입이 완료되었습니다!")

        return new_student

    def login(self, email):
        """
        학생 로그인을 처리합니다.

        Args:
        email (str): 학생 이메일.

        Returns:
        Student: 로그인된 학생 객체.
        """
        for student in self.students:
            if student.email == email:
                self.current_user = student  # 현재 사용자 설정
                print(f"👋 {student.name}님, 환영합니다!")
                return student
        print("⚠️ 이메일을 찾을 수 없습니다. 회원가입을 먼저 진행하세요.")
        return None

    def save_student(self, student):
        """
        새로운 학생 데이터를 CSV 파일에 저장합니다.

        Args:
        student (Student): 저장할 학생 객체.
        """
        try:
            df = pd.DataFrame([{
                'student_id': student.student_id,
                'name': student.name,
                'email': student.email
            }])
            df.to_csv(self.file_path, mode='a', header=False, index=False)
        except Exception as e:
            print(f"❌ 학생 데이터를 저장하는 중 오류가 발생했습니다: {e}")

    def logout(self):
        """
        로그아웃 기능을 구현합니다. 현재 로그인된 사용자 정보를 삭제합니다.
        """
        if self.current_user:
            print(f"👋 {self.current_user.name}님, 로그아웃 되었습니다.")
            self.current_user = None
        else:
            print("⚠️ 현재 로그인된 사용자가 없습니다.")

    def get_current_user(self):
        """
        현재 로그인된 사용자의 정보를 반환합니다.

        Returns:
        Student or None: 현재 로그인된 사용자 객체 또는 None.
        """
        return self.current_user