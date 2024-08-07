import pandas as pd
from record import Record
from datetime import datetime

class RecordManager:
    def __init__(self, file_path):
        """
        RecordManager 클래스 생성자.

        Args:
        file_path (str): 기록 데이터 CSV 파일 경로.
        """
        self.file_path = file_path
        self.records = self.load_records()

    def load_records(self):
        """
        CSV 파일에서 기록 데이터를 로드하여 Record 객체 리스트로 반환합니다.

        Returns:
        list of Record: 기록 객체 리스트.
        """
        records = []
        try:
            df = pd.read_csv(self.file_path)
            for _, row in df.iterrows():
                record = Record(
                    record_id=row['record_id'],
                    student_id=row['student_id'],
                    problem_id=row['problem_id'],
                    elapsed_time=row['elapsed_time'],
                    score=row['score'],
                    status=row['status'],
                    attempt_count=row['attempt_count'],
                    last_modified=datetime.strptime(row['last_modified'], "%Y-%m-%d %H:%M:%S")
                )
                records.append(record)
            return records
        except FileNotFoundError:
            print("⚠️ 기록 파일을 찾을 수 없습니다. 새로 생성됩니다.")
            return []
        except Exception as e:
            print(f"❌ 기록 데이터를 로드하는 중 오류가 발생했습니다: {e}")
            return []

    def add_record(self, student_id, problem_id, elapsed_time, score, status, attempt_count):
        """
        새로운 기록을 추가합니다.

        Args:
        student_id (int): 학생 ID.
        problem_id (int): 문제 ID.
        elapsed_time (int): 풀이 소요 시간 (초).
        score (int): 획득 점수.
        status (str): 풀이 상태.
        attempt_count (int): 시도 횟수.
        """
        new_record_id = max((record.record_id for record in self.records), default=0) + 1
        last_modified = datetime.now()

        new_record = Record(
            record_id=new_record_id,
            student_id=student_id,
            problem_id=problem_id,
            elapsed_time=elapsed_time,
            score=score,
            status=status,
            attempt_count=attempt_count,
            last_modified=last_modified
        )

        self.records.append(new_record)
        self.save_record(new_record)

    def save_record(self, record):
        """
        Record 데이터를 CSV 파일에 저장합니다.

        Args:
        record (Record): 저장할 Record 객체.
        """
        try:
            df = pd.DataFrame([record.to_dict()])
            df.to_csv(self.file_path, mode='a', header=not pd.io.common.file_exists(self.file_path), index=False)
        except Exception as e:
            print(f"❌ 기록 데이터를 저장하는 중 오류가 발생했습니다: {e}")
