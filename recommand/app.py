from flask import Flask, render_template, request, redirect, url_for, session, flash
from auth import Auth
from data_loader import DataLoader
from quiz import Quiz
from record_manager import RecordManager
from recommendation_system import RecommendationSystem

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 인스턴스 생성
auth = Auth('./students.csv')
loader = DataLoader('./problems.csv')
problems = loader.load_problems()
record_manager = RecordManager('./records.csv')
recommendation_system = RecommendationSystem('./records.csv')


# Error handler for AttributeError
@app.errorhandler(AttributeError)
def handle_attribute_error(error):
    """
    AttributeError 핸들러. 로그인 상태가 아닐 때 발생하는 오류를 처리하고 로그인 페이지로 리다이렉트합니다.
    """
    flash("세션이 만료되었거나 로그인되지 않았습니다. 다시 로그인하세요.", "danger")
    return redirect(url_for('login'))


# 전역 변수로 Quiz 인스턴스를 관리
quiz_instances = {}


@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('quiz'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        student = auth.login(email)
        if student:
            session['user_id'] = student.student_id  # 세션에 사용자 ID 저장
            flash(f"환영합니다, {student.name}!", "success")
            return redirect(url_for('quiz'))
        else:
            flash("이메일을 찾을 수 없습니다. 회원가입을 먼저 진행하세요.", "danger")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        student = auth.register(name, email)
        if student:
            flash("회원가입이 완료되었습니다. 로그인하세요.", "success")
            return redirect(url_for('login'))
        else:
            flash("이미 존재하는 이메일입니다.", "danger")
    return render_template('register.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """
    일반 문제 페이지
    """
    if 'user_id' not in session:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for('login'))

    student = auth.get_current_user()
    if not student:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for('login'))

    # Quiz 인스턴스를 전역 변수로 관리
    if student.student_id not in quiz_instances:
        quiz_instances[student.student_id] = Quiz(problems, student, record_manager)
    quiz_instance = quiz_instances[student.student_id]

    if request.method == 'POST':
        answer = request.form['answer']
        problem_id = int(request.form['problem_id'])
        quiz_instance.submit_answer(problem_id, answer)
        recommendation_system.reload()  # 문제 제출 후 추천 시스템 갱신
        return redirect(url_for('quiz'))

    problem = quiz_instance.get_random_problem()

    # 푼 문제 수 체크
    solved_problems_count = len(record_manager.get_records_by_student(student.student_id))

    # 추천 문제 가져오기
    recommended_problem_ids = []
    if solved_problems_count >= 5:
        recommended_problem_ids = recommendation_system.recommend_problems(student.student_id, top_n=5)
        print("추천 : recommended_problem_ids")

    return render_template('quiz.html', problem=problem, solved_problems_count=solved_problems_count,
                           recommended_problem_ids=recommended_problem_ids, auth=auth)


@app.route('/recommend/<int:problem_id>', methods=['GET', 'POST'])
def recommend(problem_id):
    """
    추천 문제 페이지
    """
    if 'user_id' not in session:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for('login'))

    student = auth.get_current_user()
    if not student:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for('login'))

    quiz_instance = quiz_instances[student.student_id]
    problem = quiz_instance.get_problem_by_id(problem_id)

    if request.method == 'POST':
        answer = request.form['answer']
        quiz_instance.submit_answer(problem_id, answer)
        recommendation_system.reload()  # 추천 문제 제출 후 추천 시스템 갱신

        # 추천 문제 풀기 후 다시 일반 문제 페이지로 돌아가기
        return redirect(url_for('quiz'))

    return render_template('recommend.html', problem=problem)


@app.route('/results')
def results():
    if 'user_id' not in session:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for('login'))

    current_user = auth.get_current_user()
    if current_user is None:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for('login'))

    user_records = record_manager.get_records_by_student(current_user.student_id)

    return render_template('results.html', records=user_records)


@app.route('/logout')
def logout():
    user_id = session.pop('user_id', None)  # 세션에서 사용자 ID 제거
    if user_id and user_id in quiz_instances:
        del quiz_instances[user_id]  # 전역 변수에서 퀴즈 인스턴스 제거
    flash("로그아웃 되었습니다.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0'
            , debug=True)
