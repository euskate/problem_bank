from flask import Flask, render_template, request, redirect, url_for, session, flash
from auth import Auth
from data_loader import DataLoader
from quiz import Quiz
from record_manager import RecordManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# 인스턴스 생성
auth = Auth('./students.csv')
loader = DataLoader('./problems.csv')
problems = loader.load_problems()
record_manager = RecordManager('./records.csv')

# Error handler for AttributeError
@app.errorhandler(AttributeError)
def handle_attribute_error(error):
    """
    AttributeError 핸들러. 로그인 상태가 아닐 때 발생하는 오류를 처리하고 로그인 페이지로 리다이렉트합니다.
    """
    flash("세션이 만료되었거나 로그인되지 않았습니다. 다시 로그인하세요.", "danger")
    return redirect(url_for('login'))

@app.route('/')
def home():
    """
    홈 페이지
    """
    if 'user_id' in session:
        return redirect(url_for('quiz'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    로그인 페이지
    """
    if request.method == 'POST':
        email = request.form['email']
        student = auth.login(email)
        if student:
            session['user_id'] = student.student_id
            flash(f"환영합니다, {student.name}!", "success")
            return redirect(url_for('quiz'))
        else:
            flash("이메일을 찾을 수 없습니다. 회원가입을 먼저 진행하세요.", "danger")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    회원가입 페이지
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        student = auth.register(name, email)
        if student:
            flash("회원가입이 완료되었습니다. 로그인하세요.", "success")
            return redirect(url_for('login'))
        else:
            flash("이미 존재하는 이메일입니다.", "danger")
    return rgginder_template('register.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """
    퀴즈 페이지
    """
    if 'user_id' not in session:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for('login'))

    student = auth.get_current_user()
    if not student:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for('login'))

    # Quiz 인스턴스를 지속적으로 재사용하도록 한다.
    global quiz_instance
    if 'quiz_instance' not in session:
        quiz_instance = Quiz(problems, student, record_manager)
        session['quiz_instance'] = True
    else:
        print("Quiz 인스턴스 이미 존재")  # 인스턴스 중복 생성 방지

    if request.method == 'POST':
        answer = request.form['answer']
        problem_id = int(request.form['problem_id'])
        quiz_instance.submit_answer(problem_id, answer)
        return redirect(url_for('quiz'))

    problem = quiz_instance.get_random_problem()
    return render_template('quiz.html', problem=problem)



@app.route('/results')
def results():
    """
    결과 페이지
    """
    if 'user_id' not in session:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for('login'))

    current_user = auth.get_current_user()
    if current_user is None:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for('login'))

    # 현재 사용자에 대한 기록만 가져오기
    user_records = record_manager.get_records_by_student(current_user.student_id)

    return render_template('results.html', records=user_records)

    # records = record_manager.records 전체 사용자
    # return render_template('results.html', records=records)


@app.route('/logout')
def logout():
    """
    로그아웃 처리
    """
    auth.logout()
    session.pop('user_id', None)
    flash("로그아웃 되었습니다.", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
