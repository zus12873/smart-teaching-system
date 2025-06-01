from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import os
import json
import dotenv
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from workflow_utils import upload_and_run_workflow, run_three_txt_files_workflow
from models import db, User, Role, Course, Assignment, Problem, Submission, ProblemSubmission, Enrollment

# 加载环境变量
dotenv.load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI", "sqlite:///teaching_system.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 初始化 LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录以访问此页面'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 创建数据库和管理员账号的函数
def create_tables():
    db.create_all()
    
    # 检查是否需要创建管理员用户
    if not User.query.filter_by(role=Role.ADMIN).first():
        admin = User(
            username='admin',
            email='admin@example.com',
            role=Role.ADMIN
        )
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()

# 公共路由
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin_dashboard'))
        elif current_user.is_teacher():
            return redirect(url_for('teacher_dashboard'))
        elif current_user.is_student():
            return redirect(url_for('student_dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('用户名或密码错误', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 管理员路由
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    teachers = User.query.filter_by(role=Role.TEACHER).all()
    students = User.query.filter_by(role=Role.STUDENT).all()
    courses = Course.query.all()
    
    return render_template('admin/dashboard.html', 
                          teachers=teachers, 
                          students=students, 
                          courses=courses)

@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def admin_users():
    if not current_user.is_admin():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('邮箱已存在', 'danger')
        else:
            user = User(username=username, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('用户创建成功', 'success')
            
    teachers = User.query.filter_by(role=Role.TEACHER).all()
    students = User.query.filter_by(role=Role.STUDENT).all()
    
    return render_template('admin/users.html', 
                          teachers=teachers, 
                          students=students)

@app.route('/admin/courses', methods=['GET', 'POST'])
@login_required
def admin_courses():
    if not current_user.is_admin():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    teachers = User.query.filter_by(role=Role.TEACHER).all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        teacher_id = request.form.get('teacher_id')
        
        course = Course(
            name=name,
            description=description,
            teacher_id=teacher_id
        )
        db.session.add(course)
        db.session.commit()
        flash('课程创建成功', 'success')
    
    courses = Course.query.all()
    return render_template('admin/courses.html', 
                          courses=courses, 
                          teachers=teachers)

# 课程编辑
@app.route('/admin/course/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_course(course_id):
    if not current_user.is_admin():
        flash('无权访问', 'danger')
        return redirect(url_for('index'))
    course = Course.query.get_or_404(course_id)
    teachers = User.query.filter_by(role=Role.TEACHER).all()
    if request.method == 'POST':
        course.name = request.form.get('name')
        course.description = request.form.get('description')
        course.teacher_id = request.form.get('teacher_id')
        db.session.commit()
        flash('课程信息已更新', 'success')
        return redirect(url_for('admin_courses'))
    return render_template('admin/edit_course.html', course=course, teachers=teachers)

# 课程删除
@app.route('/admin/course/<int:course_id>/delete', methods=['POST'])
@login_required
def admin_delete_course(course_id):
    if not current_user.is_admin():
        flash('无权访问', 'danger')
        return redirect(url_for('index'))
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('课程已删除', 'success')
    return redirect(url_for('admin_courses'))

# 教师路由
@app.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    if not current_user.is_teacher():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    assignments = []
    
    for course in courses:
        course_assignments = Assignment.query.filter_by(course_id=course.id).all()
        for assignment in course_assignments:
            assignments.append({
                'id': assignment.id,
                'title': assignment.title,
                'course': course.name,
                'created_at': assignment.created_at,
                'problems_count': len(assignment.problems),
                'submissions_count': len(assignment.submissions)
            })
    
    return render_template('teacher/dashboard.html', 
                          courses=courses, 
                          assignments=assignments)

@app.route('/teacher/courses')
@login_required
def teacher_courses():
    if not current_user.is_teacher():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/courses.html', courses=courses)

@app.route('/teacher/course/<int:course_id>')
@login_required
def teacher_course_detail(course_id):
    if not current_user.is_teacher():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    course = Course.query.get_or_404(course_id)
    
    if course.teacher_id != current_user.id:
        flash('无权访问此课程', 'danger')
        return redirect(url_for('teacher_courses'))
    
    assignments = Assignment.query.filter_by(course_id=course_id).all()
    
    # 获取课程的学生
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    students = [enrollment.student for enrollment in enrollments]
    # 新增：构建学生id到enrollment的映射
    student_enrollments = {enrollment.student_id: enrollment for enrollment in enrollments}
    # 获取未加入该课程的学生
    enrolled_ids = [enrollment.student_id for enrollment in enrollments]
    available_students = User.query.filter(User.role==Role.STUDENT, ~User.id.in_(enrolled_ids)).all()
    
    return render_template('teacher/course_detail.html', 
                          course=course, 
                          assignments=assignments,
                          students=students,
                          available_students=available_students,
                          student_enrollments=student_enrollments)

@app.route('/teacher/assignment/create', methods=['GET', 'POST'])
@login_required
def teacher_create_assignment():
    if not current_user.is_teacher():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        course_id = request.form.get('course_id')
        
        # 创建新作业
        assignment = Assignment(
            title=title,
            description=description,
            course_id=course_id
        )
        db.session.add(assignment)
        db.session.commit()
        
        flash('作业创建成功，请添加题目', 'success')
        return redirect(url_for('teacher_edit_assignment', assignment_id=assignment.id))
    
    return render_template('teacher/create_assignment.html', courses=courses)

@app.route('/teacher/assignment/<int:assignment_id>/edit', methods=['GET', 'POST'])
@login_required
def teacher_edit_assignment(assignment_id):
    if not current_user.is_teacher():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    if assignment.course.teacher_id != current_user.id:
        flash('无权编辑此作业', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    problems = Problem.query.filter_by(assignment_id=assignment_id).order_by(Problem.order).all()
    
    if request.method == 'POST':
        # 处理表单提交
        action = request.form.get('action', '')
        
        if action == 'add_problem':
            # 添加新题目
            problem_text = request.form.get('problem_text')
            reference_answer = request.form.get('reference_answer')
            grading_criteria = request.form.get('grading_criteria')
            
            order = Problem.query.filter_by(assignment_id=assignment_id).count() + 1
            new_problem = Problem(
                assignment_id=assignment_id,
                problem_text=problem_text,
                reference_answer=reference_answer,
                grading_criteria=grading_criteria,
                order=order
            )
            db.session.add(new_problem)
            db.session.commit()
            flash('题目添加成功', 'success')
        else:
            # 更新作业信息
            assignment.title = request.form.get('title')
            assignment.description = request.form.get('description', '')
            
            # 处理截止日期
            due_date_str = request.form.get('due_date', '')
            if due_date_str:
                try:
                    assignment.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                except ValueError:
                    flash('日期格式错误', 'danger')
            else:
                assignment.due_date = None
            
            db.session.commit()
            flash('作业信息更新成功', 'success')
        
        return redirect(url_for('teacher_edit_assignment', assignment_id=assignment_id))
    
    return render_template('teacher/edit_assignment.html', 
                          assignment=assignment,
                          problems=problems)

@app.route('/teacher/generate_problem', methods=['POST'])
@login_required
def teacher_generate_problem():
    if not current_user.is_teacher():
        return jsonify({"error": "无权访问"}), 403
    
    assignment_id = request.form.get('assignment_id')
    subject = request.form.get('subject', '计算机')
    difficulty = request.form.get('difficulty', '中等')
    
    # 获取题目类型数量
    choice_count = request.form.get('choice', '0')
    true_false_count = request.form.get('true_false', '0')
    gap_filling_count = request.form.get('gap_filling', '0')
    programming_count = request.form.get('programming', '0')
    
    # 验证至少选择了一种题型
    if int(choice_count) + int(true_false_count) + int(gap_filling_count) + int(programming_count) <= 0:
        return jsonify({"error": "请至少选择一种题型"}), 400
    
    # 获取API密钥
    api_key = os.getenv("DIFY_API_KEY_PROBLEM")
    
    # 获取生成模式
    pattern_type = request.form.get('pattern_type', '从上传题库中抽取')
    
    # 获取上传的文件（如果有）
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        temp_path = "./uploads/txt/" + file.filename
        file.save(temp_path)
    else:
        temp_path = None
        if pattern_type == '从上传题库中抽取':
            return jsonify({"error": "选择从题库抽取模式时，请上传题库文件"}), 400
    
    # 设置工作流输入参数
    workflow_inputs = {
        "choice": choice_count,
        "True_False": true_false_count,
        "Gap_filling": gap_filling_count,
        "Programming": programming_count,
        "Difficulty_Level": difficulty,
        "subject": subject,
        "Pattern_type": pattern_type
    }
    
    # 调用API生成问题
    if temp_path:
        result = upload_and_run_workflow(api_key, temp_path, workflow_inputs)
    else:
        # 对于自动生成，可能需要修改API调用
        result = upload_and_run_workflow(api_key, temp_path, workflow_inputs)
    
    if result and 'data' in result and 'outputs' in result['data']:
        print("result",result)
     
     
        outputs = result['data']['outputs']
        # 先尝试 output1，不行就用 output2
        problem_text = outputs.get('output1') or outputs.get('output2')
        if not problem_text:
            return jsonify({"error": "题目生成失败（无有效输出）"}), 500
        
        
        print("problem_text",problem_text)
        
        # 创建新问题
        order = Problem.query.filter_by(assignment_id=assignment_id).count() + 1
        problem = Problem(
            assignment_id=assignment_id,
            problem_text=problem_text,
            order=order
        )
        db.session.add(problem)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "problem": {
                "id": problem.id,
                "text": problem_text,
                "order": order
            }
        })
    else:
        return jsonify({"error": "题目生成失败"}), 500

@app.route('/teacher/problem/<int:problem_id>/edit', methods=['GET', 'POST'])
@login_required
def teacher_edit_problem(problem_id):
    if not current_user.is_teacher():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    problem = Problem.query.get_or_404(problem_id)
    
    if problem.assignment.course.teacher_id != current_user.id:
        flash('无权编辑此题目', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        problem.problem_text = request.form.get('problem_text')
        problem.reference_answer = request.form.get('reference_answer')
        problem.grading_criteria = request.form.get('grading_criteria')
        
        db.session.commit()
        flash('题目更新成功', 'success')
        return redirect(url_for('teacher_edit_assignment', assignment_id=problem.assignment_id))
    
    return render_template('teacher/edit_problem.html', problem=problem)

@app.route('/teacher/assignment/<int:assignment_id>/submissions')
@login_required
def teacher_view_submissions(assignment_id):
    if not current_user.is_teacher():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    if assignment.course.teacher_id != current_user.id:
        flash('无权查看此作业提交', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    submissions = Submission.query.filter_by(assignment_id=assignment_id).all()
    
    return render_template('teacher/view_submissions.html', 
                          assignment=assignment, 
                          submissions=submissions)

# 学生路由
@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if not current_user.is_student():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    # 获取学生选修的课程
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    courses = [enrollment.course for enrollment in enrollments]
    
    # 获取待完成的作业
    pending_assignments = []
    completed_assignments = []
    
    for course in courses:
        assignments = Assignment.query.filter_by(course_id=course.id).all()
        for assignment in assignments:
            submission = Submission.query.filter_by(
                student_id=current_user.id,
                assignment_id=assignment.id
            ).first()
            
            if submission:
                completed_assignments.append({
                    'assignment': assignment,
                    'course': course,
                    'submission': submission
                })
            else:
                pending_assignments.append({
                    'assignment': assignment,
                    'course': course
                })
    
    return render_template('student/dashboard.html', 
                          courses=courses,
                          pending_assignments=pending_assignments,
                          completed_assignments=completed_assignments)

@app.route('/student/assignment/<int:assignment_id>')
@login_required
def student_view_assignment(assignment_id):
    if not current_user.is_student():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # 检查学生是否选修了该课程
    enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=assignment.course_id
    ).first()
    
    if not enrollment:
        flash('您未选修该课程', 'danger')
        return redirect(url_for('student_dashboard'))
    
    # 获取学生的提交
    submission = Submission.query.filter_by(
        student_id=current_user.id,
        assignment_id=assignment_id
    ).first()
    
    problems = Problem.query.filter_by(assignment_id=assignment_id).order_by(Problem.order).all()
    
    # 获取每个问题的提交情况
    problem_submissions = {}
    if submission:
        for problem in problems:
            prob_sub = ProblemSubmission.query.filter_by(
                submission_id=submission.id,
                problem_id=problem.id
            ).first()
            problem_submissions[problem.id] = prob_sub
    
    return render_template('student/view_assignment.html', 
                          assignment=assignment,
                          problems=problems,
                          submission=submission,
                          problem_submissions=problem_submissions)

@app.route('/student/assignment/<int:assignment_id>/submit', methods=['POST'])
@login_required
def student_submit_assignment(assignment_id):
    if not current_user.is_student():
        return jsonify({"error": "无权访问"}), 403
    assignment = Assignment.query.get_or_404(assignment_id)
    # 检查学生是否选修了该课程
    enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=assignment.course_id
    ).first()
    if not enrollment:
        return jsonify({"error": "您未选修该课程"}), 403
    data = request.get_json()
    answers = data.get('answers', {})
    problems = Problem.query.filter_by(assignment_id=assignment_id).all()
    # 获取或创建提交记录
    submission = Submission.query.filter_by(
        student_id=current_user.id,
        assignment_id=assignment_id
    ).first()
    if not submission:
        submission = Submission(
            student_id=current_user.id,
            assignment_id=assignment_id
        )
        db.session.add(submission)
        db.session.commit()
    # 依次保存每道题答案并判分
    api_key = os.getenv("DIFY_API_KEY_MARKING")
    os.makedirs("./uploads/txt", exist_ok=True)
    for problem in problems:
        ans = answers.get(str(problem.id), "")
        if not ans:
            continue
        problem_submission = ProblemSubmission.query.filter_by(
            submission_id=submission.id,
            problem_id=problem.id
        ).first()
        if not problem_submission:
            problem_submission = ProblemSubmission(
                submission_id=submission.id,
                problem_id=problem.id
            )
            db.session.add(problem_submission)
        problem_submission.answer = ans
        # 判分
        student_file = f"./uploads/txt/student_{problem.id}.txt"
        problem_file = f"./uploads/txt/problem_{problem.id}.txt"
        criteria_file = f"./uploads/txt/criteria_{problem.id}.txt"
        with open(student_file, 'w') as f:
            f.write(ans)
        with open(problem_file, 'w') as f:
            f.write(problem.problem_text)
        with open(criteria_file, 'w') as f:
            f.write(problem.grading_criteria or "根据代码逻辑和功能完成度进行评分。")
        result = run_three_txt_files_workflow(api_key, student_file, problem_file, criteria_file)
        if result and 'data' in result and 'outputs' in result['data']:
            output = result['data']['outputs'].get('output', '')
            problem_submission.grading_result = output
            # 尝试提取分数
            score = 0
            try:
                import re
                score_match = re.search(r'分数.*?(\d+)/(\d+)', output)
                if score_match:
                    score = float(score_match.group(1))
            except:
                score = 0
            problem_submission.score = score
        else:
            problem_submission.grading_result = '评分失败'
            problem_submission.score = 0
        db.session.commit()
    # 更新作业总分
    update_submission_total_score(submission.id)
    return jsonify({"success": True})

def update_submission_total_score(submission_id):
    """更新作业总分"""
    submission = Submission.query.get(submission_id)
    problem_submissions = ProblemSubmission.query.filter_by(submission_id=submission_id).all()
    
    total_score = sum(ps.score or 0 for ps in problem_submissions)
    total_problems = len(problem_submissions)
    
    if total_problems > 0:
        submission.total_score = total_score / total_problems
    else:
        submission.total_score = 0
    
    submission.is_graded = all(ps.score is not None for ps in problem_submissions)
    db.session.commit()

@app.route('/problem_generation', methods=['GET'])
def problem_generation():
    return render_template('problem_generation.html')

# 保留原有的AI接口路由
@app.route('/run_workflow', methods=['POST'])
def run_workflow():
    # 获取API密钥
    api_key = os.getenv("DIFY_API_KEY_PROBLEM")
    
    # 获取上传的文件
    if 'file' not in request.files:
        return jsonify({"error": "没有上传文件"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400
    
    # 保存文件到临时位置
    temp_path = "./uploads/txt/" + file.filename
    file.save(temp_path)
    
    # 获取表单参数
    workflow_inputs = {
        "choice": request.form.get('choice', '1'),
        "True_False": request.form.get('true_false', '1'),
        "Difficulty_Level": request.form.get('difficulty', '简单'),
        "subject": request.form.get('subject', '计算机'),
        "Gap_filling": request.form.get('gap_filling', '1'),
        "Programming": request.form.get('programming', '1'),
        "Pattern_type": request.form.get('pattern_type', '从上传题库中抽取')
    }

    # 调用API
    result = upload_and_run_workflow(api_key, temp_path, workflow_inputs)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "API调用失败"}), 500

@app.route('/run_multi_workflow', methods=['POST'])
def run_multi_workflow():
    # 获取API密钥
    api_key = os.getenv("DIFY_API_KEY_MARKING")
    
    # 检查是否有3个文件上传
    if 'file1' not in request.files or 'file2' not in request.files or 'file3' not in request.files:
        return jsonify({"error": "需要上传3个文件"}), 400
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    file3 = request.files['file3']
    
    # 检查文件是否选择
    if file1.filename == '' or file2.filename == '' or file3.filename == '':
        return jsonify({"error": "请选择所有3个文件"}), 400
    
    # 保存文件到临时位置
    os.makedirs("./uploads/txt", exist_ok=True)
    temp_path1 = "./uploads/txt/" + file1.filename
    temp_path2 = "./uploads/txt/" + file2.filename
    temp_path3 = "./uploads/txt/" + file3.filename
    
    file1.save(temp_path1)
    file2.save(temp_path2)
    file3.save(temp_path3)
    
    # 调用API
    result = run_three_txt_files_workflow(api_key, temp_path1, temp_path2, temp_path3)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "API调用失败"}), 500

@app.route('/multi_upload', methods=['GET'])
def multi_upload():
    return render_template('multi_upload.html')

@app.route('/api/teacher/courses', methods=['GET'])
@login_required
def teacher_courses_api():
    if not current_user.is_teacher():
        return jsonify({"error": "无权访问"}), 403
    
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    courses_data = [{"id": course.id, "name": course.name} for course in courses]
    
    return jsonify({
        "success": True,
        "courses": courses_data
    })

@app.route('/api/save_generated_assignment', methods=['POST'])
@login_required
def save_generated_assignment():
    if not current_user.is_teacher():
        return jsonify({"error": "无权访问"}), 403
    
    data = request.json
    
    title = data.get('title')
    course_id = data.get('course_id')
    description = data.get('description', '')
    due_date_str = data.get('due_date')
    problem_content = data.get('problem_content')
    
    # 验证必要字段
    if not title or not course_id or not problem_content:
        return jsonify({"error": "缺少必要信息"}), 400
    
    # 检查课程是否存在且属于当前教师
    course = Course.query.get(course_id)
    if not course or course.teacher_id != current_user.id:
        return jsonify({"error": "课程不存在或无权操作"}), 403
    
    # 处理日期
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "日期格式错误"}), 400
    
    # 创建新作业
    assignment = Assignment(
        title=title,
        description=description,
        course_id=course_id,
        due_date=due_date,
        created_at=datetime.now()
    )
    db.session.add(assignment)
    db.session.flush()  # 获取ID但不提交
    
    # 创建题目
    problem = Problem(
        assignment_id=assignment.id,
        problem_text=problem_content,
        order=1
    )
    db.session.add(problem)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "assignment_id": assignment.id,
        "course_name": course.name,
        "assignment_url": url_for('teacher_edit_assignment', assignment_id=assignment.id)
    })

@app.route('/teacher/course/<int:course_id>/enroll', methods=['POST'])
@login_required
def teacher_enroll_student(course_id):
    if not current_user.is_teacher():
        flash('无权访问此页面', 'danger')
        return redirect(url_for('index'))
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        flash('无权操作此课程', 'danger')
        return redirect(url_for('teacher_courses'))
    student_id = request.form.get('student_id')
    student = User.query.filter_by(id=student_id, role=Role.STUDENT).first()
    if not student:
        flash('学生不存在', 'danger')
        return redirect(url_for('teacher_course_detail', course_id=course_id))
    # 检查是否已选课
    exists = Enrollment.query.filter_by(student_id=student.id, course_id=course_id).first()
    if exists:
        flash('该学生已在课程中', 'warning')
        return redirect(url_for('teacher_course_detail', course_id=course_id))
    enrollment = Enrollment(student_id=student.id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    flash('学生添加成功', 'success')
    return redirect(url_for('teacher_course_detail', course_id=course_id))

# 用户编辑
@app.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    if not current_user.is_admin():
        flash('无权访问', 'danger')
        return redirect(url_for('index'))
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        role = request.form.get('role')
        if role in [Role.ADMIN, Role.TEACHER, Role.STUDENT]:
            user.role = role
        password = request.form.get('password')
        if password:
            user.set_password(password)
        db.session.commit()
        flash('用户信息已更新', 'success')
        return redirect(url_for('admin_users'))
    return render_template('admin/edit_user.html', user=user)

# 用户删除
@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin():
        flash('无权访问', 'danger')
        return redirect(url_for('index'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('用户已删除', 'success')
    return redirect(url_for('admin_users'))

if __name__ == "__main__":
    # 确保上传目录存在
    os.makedirs("./uploads/txt", exist_ok=True)
    
    # 初始化数据库和管理员账号
    with app.app_context():
        create_tables()
        
    # 运行应用
    app.run(debug=True)