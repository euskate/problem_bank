from datetime import datetime

class Record:
    def __init__(self, record_id, student_id, problem_id, elapsed_time, score, status, attempt_count, last_modified):
        """
        Record 클래스 생성자.

        Args:
        record_id (int): 기록 ID.
        student_id (int): 학생 ID.
        problem_id (int): 문제 ID.
        elapsed_time (int): 풀이 소요 시간 (초).
        score (int): 획득 점수.
        status (str): 풀이 상태 ("정답", "오답", "부분 정답", "미제출").
        attempt_count (int): 시도 횟수.
        last_modified (datetime): 마지막 수정 시간.
        """
        self.record_id = record_id
        self.student_id = student_id
        self.problem_id = problem_id
        self.elapsed_time = elapsed_time
        self.score = score
        self.status = status
        self.attempt_count = attempt_count
        self.last_modified = last_modified

    def to_dict(self):
        """
        Record 객체를 딕셔너리로 변환합니다.

        Returns:
        dict: Record 정보를 포함하는 딕셔너리.
        """
        return {
            'record_id': self.record_id,
            'student_id': self.student_id,
            'problem_id': self.problem_id,
            'elapsed_time': self.elapsed_time,
            'score': self.score,
            'status': self.status,
            'attempt_count': self.attempt_count,
            'last_modified': self.last_modified.strftime("%Y-%m-%d %H:%M:%S")
        }
