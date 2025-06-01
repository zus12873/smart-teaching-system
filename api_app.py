from flask import Flask, request, jsonify
from flask_cors import CORS
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

# 配置CORS支持Vue前端
CORS(
    app,
    origins=['http://localhost:5173', 'http://localhost:5174', 'http://127.0.0.1:5173', 'http://127.0.0.1:5174'],
    supports_credentials=True,
    allow_headers=['Content-Type', 'Authorization', 'X-Requested-With', 'Accept'],
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    expose_headers=['Set-Cookie']
)

# 配置会话cookie
app.config['SESSION_COOKIE_SAMESITE'] = None   # 允许跨域
app.config['SESSION_COOKIE_SECURE'] = False    # 开发环境使用HTTP
app.config['SESSION_COOKIE_HTTPONLY'] = False  # 允许JavaScript访问（仅开发环境）
app.config['SESSION_COOKIE_DOMAIN'] = None     # 不限制域名

# 初始化数据库
db.init_app(app)

# 初始化 LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = '请先登录以访问此页面'

# 自定义未授权处理器，返回JSON而不是重定向
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"success": False, "message": "未登录或会话已过期"}), 401

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

        # 创建测试教师账号
        teacher = User(
            username='teacher',
            email='teacher@example.com',
            role=Role.TEACHER
        )
        teacher.set_password('teacher')
        db.session.add(teacher)

        # 创建测试学生账号
        student = User(
            username='student',
            email='student@example.com',
            role=Role.STUDENT
        )
        student.set_password('student')
        db.session.add(student)

        db.session.commit()
        print("✅ 创建了默认用户账号:")
        print("   管理员: admin/admin")
        print("   教师: teacher/teacher")
        print("   学生: student/student")

# ==================== 认证相关API ====================

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """用户登录API"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user, remember=True)  # 添加 remember=True

        # 添加更详细的调试信息
        from flask import session
        print(f"用户 {user.username} 登录成功")
        print(f"会话ID: {session.get('_id', '无')}")
        print(f"用户ID: {session.get('_user_id', '无')}")
        print(f"Request headers: {dict(request.headers)}")

        response = jsonify({
            "success": True,
            "message": "登录成功",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        })

        # 确保会话cookie被正确设置
        response.headers['Cache-Control'] = 'no-cache'
        return response
    else:
        return jsonify({"success": False, "message": "用户名或密码错误"}), 401

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def api_logout():
    """用户登出API"""
    logout_user()
    return jsonify({"success": True, "message": "登出成功"})

@app.route('/api/auth/current', methods=['GET'])
def api_current_user():
    """获取当前用户信息"""
    if current_user.is_authenticated:
        return jsonify({
            "success": True,
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "role": current_user.role
            }
        })
    else:
        return jsonify({"success": False, "message": "未登录"}), 401

# ==================== 管理员API ====================

@app.route('/api/admin/dashboard', methods=['GET'])
@login_required
def api_admin_dashboard():
    """管理员仪表板数据"""
    # 添加调试信息
    print(f"仪表板请求 - 当前用户: {current_user}, 认证状态: {current_user.is_authenticated}")

    if not current_user.is_admin():
        print(f"用户 {current_user.username} 不是管理员，角色: {current_user.role}")
        return jsonify({"success": False, "message": "无权访问"}), 403

    teachers = User.query.filter_by(role=Role.TEACHER).all()
    students = User.query.filter_by(role=Role.STUDENT).all()
    courses = Course.query.all()

    # 最近添加的教师和课程
    recent_teachers = User.query.filter_by(role=Role.TEACHER).order_by(User.id.desc()).limit(5).all()
    recent_courses = Course.query.order_by(Course.id.desc()).limit(5).all()

    return jsonify({
        "success": True,
        "data": {
            "stats": {
                "teachers_count": len(teachers),
                "students_count": len(students),
                "courses_count": len(courses)
            },
            "recent_teachers": [
                {
                    "id": t.id,
                    "username": t.username,
                    "email": t.email,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                } for t in recent_teachers
            ],
            "recent_courses": [
                {
                    "id": c.id,
                    "name": c.name,
                    "teacher_name": c.teacher.username if c.teacher else "未分配",
                    "teacher": {"username": c.teacher.username} if c.teacher else None,
                    "created_at": c.created_at.isoformat() if c.created_at else None
                } for c in recent_courses
            ]
        }
    })

@app.route('/api/admin/users', methods=['GET', 'POST'])
@login_required
def api_admin_users():
    """用户管理API"""
    if not current_user.is_admin():
        return jsonify({"success": False, "message": "无权访问"}), 403

    if request.method == 'GET':
        teachers = User.query.filter_by(role=Role.TEACHER).all()
        students = User.query.filter_by(role=Role.STUDENT).all()

        return jsonify({
            "success": True,
            "data": {
                "teachers": [
                    {
                        "id": t.id,
                        "username": t.username,
                        "email": t.email,
                        "role": t.role,
                        "created_at": t.created_at.isoformat() if hasattr(t, 'created_at') and t.created_at else None
                    } for t in teachers
                ],
                "students": [
                    {
                        "id": s.id,
                        "username": s.username,
                        "email": s.email,
                        "role": s.role,
                        "created_at": s.created_at.isoformat() if hasattr(s, 'created_at') and s.created_at else None
                    } for s in students
                ]
            }
        })

    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # 验证数据
        if not all([username, email, password, role]):
            return jsonify({"success": False, "message": "所有字段都是必填的"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"success": False, "message": "用户名已存在"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "邮箱已存在"}), 400

        # 创建用户
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "用户创建成功",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        })

@app.route('/api/admin/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_admin_user_detail(user_id):
    """用户详情API"""
    if not current_user.is_admin():
        return jsonify({"success": False, "message": "无权访问"}), 403

    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        return jsonify({
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        })

    elif request.method == 'PUT':
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)

        role = data.get('role')
        if role in [Role.ADMIN, Role.TEACHER, Role.STUDENT]:
            user.role = role

        password = data.get('password')
        if password:
            user.set_password(password)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "用户信息已更新",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        })

    elif request.method == 'DELETE':
        try:
            # 检查用户类型并处理关联数据
            if user.role == Role.TEACHER:
                # 处理教师删除：检查关联的课程
                courses = Course.query.filter_by(teacher_id=user.id).all()
                if courses:
                    # 如果有其他教师，可以选择转移课程，这里简单处理为删除课程
                    other_teachers = User.query.filter(
                        User.role == Role.TEACHER,
                        User.id != user.id
                    ).first()

                    if other_teachers:
                        # 转移课程到其他教师
                        for course in courses:
                            course.teacher_id = other_teachers.id
                    else:
                        # 没有其他教师，删除相关课程和数据
                        for course in courses:
                            # 删除课程相关的注册记录
                            Enrollment.query.filter_by(course_id=course.id).delete()
                            # 删除课程相关的作业和提交
                            assignments = Assignment.query.filter_by(course_id=course.id).all()
                            for assignment in assignments:
                                # 删除作业的题目提交
                                problems = Problem.query.filter_by(assignment_id=assignment.id).all()
                                for problem in problems:
                                    ProblemSubmission.query.filter_by(problem_id=problem.id).delete()
                                # 删除作业提交
                                Submission.query.filter_by(assignment_id=assignment.id).delete()
                                # 删除题目
                                Problem.query.filter_by(assignment_id=assignment.id).delete()
                                # 删除作业
                                db.session.delete(assignment)
                            # 删除课程
                            db.session.delete(course)

            elif user.role == Role.STUDENT:
                # 处理学生删除：删除相关的注册记录和提交记录
                # 删除注册记录
                Enrollment.query.filter_by(student_id=user.id).delete()
                # 删除提交记录
                submissions = Submission.query.filter_by(student_id=user.id).all()
                for submission in submissions:
                    # 删除题目提交
                    ProblemSubmission.query.filter_by(submission_id=submission.id).delete()
                    # 删除作业提交
                    db.session.delete(submission)

            # 刷新到数据库以确保外键约束
            db.session.flush()

            # 删除用户
            db.session.delete(user)
            db.session.commit()

            return jsonify({"success": True, "message": "用户已删除"})

        except Exception as e:
            db.session.rollback()
            print(f"删除用户失败: {e}")
            return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500

@app.route('/api/admin/courses', methods=['GET', 'POST'])
@login_required
def api_admin_courses():
    """课程管理API"""
    if not current_user.is_admin():
        return jsonify({"success": False, "message": "无权访问"}), 403

    if request.method == 'GET':
        courses = Course.query.all()
        teachers = User.query.filter_by(role=Role.TEACHER).all()

        return jsonify({
            "success": True,
            "data": {
                "courses": [
                    {
                        "id": c.id,
                        "name": c.name,
                        "description": c.description,
                        "teacher_id": c.teacher_id,
                        "teacher_name": c.teacher.username if c.teacher else "未分配",
                        "students_count": len(c.enrollments)
                    } for c in courses
                ],
                "teachers": [
                    {
                        "id": t.id,
                        "username": t.username
                    } for t in teachers
                ]
            }
        })

    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        teacher_id = data.get('teacher_id')

        if not name:
            return jsonify({"success": False, "message": "课程名称不能为空"}), 400

        course = Course(
            name=name,
            description=description,
            teacher_id=teacher_id
        )
        db.session.add(course)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "课程创建成功",
            "course": {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "teacher_id": course.teacher_id,
                "teacher_name": course.teacher.username if course.teacher else "未分配"
            }
        })

@app.route('/api/admin/courses/<int:course_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_admin_course_detail(course_id):
    """课程详情API"""
    if not current_user.is_admin():
        return jsonify({"success": False, "message": "无权访问"}), 403

    course = Course.query.get_or_404(course_id)

    if request.method == 'GET':
        return jsonify({
            "success": True,
            "course": {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "teacher_id": course.teacher_id,
                "teacher_name": course.teacher.username if course.teacher else "未分配"
            }
        })

    elif request.method == 'PUT':
        data = request.get_json()
        course.name = data.get('name', course.name)
        course.description = data.get('description', course.description)
        course.teacher_id = data.get('teacher_id', course.teacher_id)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "课程信息已更新",
            "course": {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "teacher_id": course.teacher_id,
                "teacher_name": course.teacher.username if course.teacher else "未分配"
            }
        })

    elif request.method == 'DELETE':
        db.session.delete(course)
        db.session.commit()
        return jsonify({"success": True, "message": "课程已删除"})

# ==================== 教师API ====================

@app.route('/api/teacher/dashboard', methods=['GET'])
@login_required
def api_teacher_dashboard():
    """教师仪表板API"""
    if not current_user.is_teacher():
        return jsonify({"success": False, "message": "无权访问"}), 403

    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    assignments = []

    for course in courses:
        course_assignments = Assignment.query.filter_by(course_id=course.id).all()
        for assignment in course_assignments:
            assignments.append({
                'id': assignment.id,
                'title': assignment.title,
                'course': course.name,
                'course_id': course.id,
                'created_at': assignment.created_at.isoformat() if assignment.created_at else None,
                'due_date': assignment.due_date.isoformat() if assignment.due_date else None,
                'problems_count': len(assignment.problems),
                'submissions_count': len(assignment.submissions)
            })

    return jsonify({
        "success": True,
        "data": {
            "courses": [
                {
                    "id": c.id,
                    "name": c.name,
                    "description": c.description,
                    "students_count": len(c.enrollments),
                    "assignments_count": len(c.assignments)
                } for c in courses
            ],
            "assignments": assignments,
            "stats": {
                "courses_count": len(courses),
                "assignments_count": len(assignments),
                "total_students": sum(len(c.enrollments) for c in courses)
            }
        }
    })

@app.route('/api/teacher/courses', methods=['GET'])
@login_required
def api_teacher_courses():
    """教师课程列表API"""
    if not current_user.is_teacher():
        return jsonify({"success": False, "message": "无权访问"}), 403

    courses = Course.query.filter_by(teacher_id=current_user.id).all()

    return jsonify({
        "success": True,
        "courses": [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "students_count": len(c.enrollments),
                "assignments_count": len(c.assignments),
                "created_at": c.created_at.isoformat() if hasattr(c, 'created_at') and c.created_at else None
            } for c in courses
        ]
    })

@app.route('/api/teacher/courses/<int:course_id>', methods=['GET'])
@login_required
def api_teacher_course_detail(course_id):
    """教师课程详情API"""
    if not current_user.is_teacher():
        return jsonify({"success": False, "message": "无权访问"}), 403

    course = Course.query.get_or_404(course_id)

    if course.teacher_id != current_user.id:
        return jsonify({"success": False, "message": "无权访问此课程"}), 403

    # 获取课程的学生
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    students = [
        {
            "id": enrollment.student.id,
            "username": enrollment.student.username,
            "email": enrollment.student.email,
            "enrollment_date": enrollment.enrolled_at.isoformat() if enrollment.enrolled_at else None
        } for enrollment in enrollments
    ]

    # 获取未加入该课程的学生
    enrolled_ids = [enrollment.student_id for enrollment in enrollments]
    if enrolled_ids:
        available_students = User.query.filter(
            User.role == Role.STUDENT,
            ~User.id.in_(enrolled_ids)
        ).all()
    else:
        available_students = User.query.filter(User.role == Role.STUDENT).all()

    # 获取课程作业
    assignments = Assignment.query.filter_by(course_id=course_id).all()

    return jsonify({
        "success": True,
        "data": {
            "course": {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "teacher_id": course.teacher_id
            },
            "students": students,
            "available_students": [
                {
                    "id": s.id,
                    "username": s.username,
                    "email": s.email
                } for s in available_students
            ],
            "assignments": [
                {
                    "id": a.id,
                    "title": a.title,
                    "description": a.description,
                    "created_at": a.created_at.isoformat() if a.created_at else None,
                    "due_date": a.due_date.isoformat() if a.due_date else None,
                    "problems_count": len(a.problems),
                    "submissions_count": len(a.submissions)
                } for a in assignments
            ]
        }
    })

@app.route('/api/teacher/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
def api_teacher_enroll_student(course_id):
    """添加学生到课程API"""
    if not current_user.is_teacher():
        return jsonify({"success": False, "message": "无权访问"}), 403

    course = Course.query.get_or_404(course_id)

    if course.teacher_id != current_user.id:
        return jsonify({"success": False, "message": "无权操作此课程"}), 403

    data = request.get_json()
    student_id = data.get('student_id')

    if not student_id:
        return jsonify({"success": False, "message": "学生ID不能为空"}), 400

    student = User.query.get_or_404(student_id)

    if student.role != Role.STUDENT:
        return jsonify({"success": False, "message": "只能添加学生用户"}), 400

    # 检查是否已经注册
    existing = Enrollment.query.filter_by(course_id=course_id, student_id=student_id).first()
    if existing:
        return jsonify({"success": False, "message": "学生已在该课程中"}), 400

    # 创建注册记录
    enrollment = Enrollment(course_id=course_id, student_id=student_id)
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "学生添加成功",
        "student": {
            "id": student.id,
            "username": student.username,
            "email": student.email
        }
    })

@app.route('/api/teacher/courses/<int:course_id>/enroll/<int:student_id>', methods=['DELETE'])
@login_required
def api_teacher_unenroll_student(course_id, student_id):
    """从课程中移除学生API"""
    if not current_user.is_teacher():
        return jsonify({"success": False, "message": "无权访问"}), 403

    course = Course.query.get_or_404(course_id)

    if course.teacher_id != current_user.id:
        return jsonify({"success": False, "message": "无权操作此课程"}), 403

    enrollment = Enrollment.query.filter_by(course_id=course_id, student_id=student_id).first()

    if not enrollment:
        return jsonify({"success": False, "message": "学生不在该课程中"}), 404

    db.session.delete(enrollment)
    db.session.commit()

    return jsonify({"success": True, "message": "学生移除成功"})

@app.route('/api/teacher/assignments', methods=['GET', 'POST'])
@login_required
def api_teacher_assignments():
    """教师作业管理API"""
    if not current_user.is_teacher():
        return jsonify({"success": False, "message": "无权访问"}), 403

    if request.method == 'GET':
        # 获取教师的所有作业
        courses = Course.query.filter_by(teacher_id=current_user.id).all()
        course_ids = [course.id for course in courses]
        assignments = Assignment.query.filter(Assignment.course_id.in_(course_ids)).all()

        return jsonify({
            "success": True,
            "assignments": [
                {
                    "id": a.id,
                    "title": a.title,
                    "description": a.description,
                    "course_id": a.course_id,
                    "course_name": a.course.name,
                    "created_at": a.created_at.isoformat() if a.created_at else None,
                    "due_date": a.due_date.isoformat() if a.due_date else None,
                    "problems_count": len(a.problems),
                    "submissions_count": len(a.submissions)
                } for a in assignments
            ]
        })

    elif request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        description = data.get('description', '')
        course_id = data.get('course_id')
        due_date_str = data.get('due_date')

        if not title or not course_id:
            return jsonify({"success": False, "message": "标题和课程不能为空"}), 400

        # 验证课程是否属于当前教师
        course = Course.query.get(course_id)
        if not course or course.teacher_id != current_user.id:
            return jsonify({"success": False, "message": "课程不存在或无权操作"}), 403

        # 处理截止日期
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"success": False, "message": "日期格式错误"}), 400

        # 创建作业
        assignment = Assignment(
            title=title,
            description=description,
            course_id=course_id,
            due_date=due_date,
            created_at=datetime.now()
        )
        db.session.add(assignment)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "作业创建成功",
            "assignment": {
                "id": assignment.id,
                "title": assignment.title,
                "description": assignment.description,
                "course_id": assignment.course_id,
                "course_name": assignment.course.name,
                "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                "created_at": assignment.created_at.isoformat()
            }
        })

@app.route('/api/teacher/assignments/<int:assignment_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_teacher_assignment_detail(assignment_id):
    """教师作业详情API"""
    if not current_user.is_teacher():
        return jsonify({"success": False, "message": "无权访问"}), 403

    assignment = Assignment.query.get_or_404(assignment_id)

    if assignment.course.teacher_id != current_user.id:
        return jsonify({"success": False, "message": "无权访问此作业"}), 403

    if request.method == 'GET':
        problems = Problem.query.filter_by(assignment_id=assignment_id).order_by(Problem.order).all()

        return jsonify({
            "success": True,
            "assignment": {
                "id": assignment.id,
                "title": assignment.title,
                "description": assignment.description,
                "course_id": assignment.course_id,
                "course_name": assignment.course.name,
                "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                "created_at": assignment.created_at.isoformat() if assignment.created_at else None,
                "problems": [
                    {
                        "id": p.id,
                        "problem_text": p.problem_text,
                        "reference_answer": p.reference_answer,
                        "grading_criteria": p.grading_criteria,
                        "order": p.order
                    } for p in problems
                ]
            }
        })

    elif request.method == 'PUT':
        data = request.get_json()
        assignment.title = data.get('title', assignment.title)
        assignment.description = data.get('description', assignment.description)

        # 处理截止日期
        due_date_str = data.get('due_date')
        if due_date_str:
            try:
                assignment.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"success": False, "message": "日期格式错误"}), 400
        elif due_date_str == '':
            assignment.due_date = None

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "作业更新成功",
            "assignment": {
                "id": assignment.id,
                "title": assignment.title,
                "description": assignment.description,
                "due_date": assignment.due_date.isoformat() if assignment.due_date else None
            }
        })

    elif request.method == 'DELETE':
        # 删除相关的题目和提交记录
        problems = Problem.query.filter_by(assignment_id=assignment_id).all()
        
        # 删除题目提交记录
        for problem in problems:
            ProblemSubmission.query.filter_by(problem_id=problem.id).delete()
        
        # 删除题目
        Problem.query.filter_by(assignment_id=assignment_id).delete()
        
        # 删除作业提交记录
        Submission.query.filter_by(assignment_id=assignment_id).delete()

        db.session.delete(assignment)
        db.session.commit()

        return jsonify({"success": True, "message": "作业删除成功"})

@app.route('/api/teacher/assignments/<int:assignment_id>/problems', methods=['POST'])
@login_required
def api_teacher_add_problem(assignment_id):
    """添加题目到作业API"""
    if not current_user.is_teacher():
        return jsonify({"success": False, "message": "无权访问"}), 403

    assignment = Assignment.query.get_or_404(assignment_id)

    if assignment.course.teacher_id != current_user.id:
        return jsonify({"success": False, "message": "无权操作此作业"}), 403

    data = request.get_json()
    problem_text = data.get('problem_text')
    reference_answer = data.get('reference_answer', '')
    grading_criteria = data.get('grading_criteria', '')

    if not problem_text:
        return jsonify({"success": False, "message": "题目内容不能为空"}), 400

    # 获取下一个排序号
    order = Problem.query.filter_by(assignment_id=assignment_id).count() + 1

    problem = Problem(
        assignment_id=assignment_id,
        problem_text=problem_text,
        reference_answer=reference_answer,
        grading_criteria=grading_criteria,
        order=order
    )
    db.session.add(problem)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "题目添加成功",
        "problem": {
            "id": problem.id,
            "problem_text": problem.problem_text,
            "reference_answer": problem.reference_answer,
            "grading_criteria": problem.grading_criteria,
            "order": problem.order
        }
    })

@app.route('/api/teacher/problems/<int:problem_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_teacher_problem_detail(problem_id):
    """教师题目详情API"""
    if not current_user.is_teacher():
        return jsonify({"success": False, "message": "无权访问"}), 403

    problem = Problem.query.get_or_404(problem_id)

    if problem.assignment.course.teacher_id != current_user.id:
        return jsonify({"success": False, "message": "无权操作此题目"}), 403

    if request.method == 'GET':
        return jsonify({
            "success": True,
            "problem": {
                "id": problem.id,
                "problem_text": problem.problem_text,
                "reference_answer": problem.reference_answer,
                "grading_criteria": problem.grading_criteria,
                "order": problem.order,
                "assignment_id": problem.assignment_id,
                "assignment_title": problem.assignment.title
            }
        })

    elif request.method == 'PUT':
        data = request.get_json()
        problem.problem_text = data.get('problem_text', problem.problem_text)
        problem.reference_answer = data.get('reference_answer', problem.reference_answer)
        problem.grading_criteria = data.get('grading_criteria', problem.grading_criteria)
        # 添加对order字段的更新
        if 'order' in data:
            problem.order = data.get('order')

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "题目更新成功",
            "problem": {
                "id": problem.id,
                "problem_text": problem.problem_text,
                "reference_answer": problem.reference_answer,
                "grading_criteria": problem.grading_criteria,
                "order": problem.order
            }
        })

    elif request.method == 'DELETE':
        # 删除相关的题目提交记录
        ProblemSubmission.query.filter_by(problem_id=problem_id).delete()

        db.session.delete(problem)
        db.session.commit()

        return jsonify({"success": True, "message": "题目删除成功"})

@app.route('/api/teacher/generate_problem', methods=['POST'])
@login_required
def api_teacher_generate_problem():
    """智能生成题目API"""
    if not current_user.is_teacher():
        return jsonify({"success": False, "message": "无权访问"}), 403

    # 获取JSON数据
    if request.content_type == 'application/json':
        data = request.get_json()
        assignment_id = data.get('assignment_id')
        subject = data.get('subject', '计算机')
        difficulty = data.get('difficulty', '中等')
        choice_count = data.get('choice', '0')
        true_false_count = data.get('true_false', '0')
        gap_filling_count = data.get('gap_filling', '0')
        programming_count = data.get('programming', '0')
        pattern_type = data.get('pattern_type', '从上传题库中抽取')
        file_content = data.get('file_content')  # Base64编码的文件内容
    else:
        # 表单数据（保持兼容性）
        assignment_id = request.form.get('assignment_id')
        subject = request.form.get('subject', '计算机')
        difficulty = request.form.get('difficulty', '中等')
        choice_count = request.form.get('choice', '0')
        true_false_count = request.form.get('true_false', '0')
        gap_filling_count = request.form.get('gap_filling', '0')
        programming_count = request.form.get('programming', '0')
        pattern_type = request.form.get('pattern_type', '从上传题库中抽取')
        file_content = None

    # 验证作业权限
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.course.teacher_id != current_user.id:
        return jsonify({"success": False, "message": "无权操作此作业"}), 403

    # 验证至少选择了一种题型
    if int(choice_count) + int(true_false_count) + int(gap_filling_count) + int(programming_count) <= 0:
        return jsonify({"success": False, "message": "请至少选择一种题型"}), 400

    # 获取API密钥
    api_key = os.getenv("DIFY_API_KEY_PROBLEM")

    # 处理文件上传
    temp_path = None
    if request.content_type != 'application/json' and 'file' in request.files and request.files['file'].filename != '':
        # 表单文件上传
        file = request.files['file']
        temp_path = "./uploads/txt/" + file.filename
        file.save(temp_path)
    elif file_content:
        # JSON中的文件内容（Base64编码）
        import base64
        try:
            file_data = base64.b64decode(file_content.split(',')[1])  # 移除data:前缀
            temp_path = f"./uploads/txt/upload_{assignment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(temp_path, 'wb') as f:
                f.write(file_data)
        except Exception as e:
            return jsonify({"success": False, "message": f"文件处理失败: {str(e)}"}), 400

    # 验证文件
    if pattern_type == '从上传题库中抽取' and not temp_path:
        return jsonify({"success": False, "message": "选择从题库抽取模式时，请上传题库文件"}), 400

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

    try:
        # 调用API生成问题
        result = upload_and_run_workflow(api_key, temp_path, workflow_inputs)

        if result and 'data' in result and 'outputs' in result['data']:
            outputs = result['data']['outputs']
            # 先尝试 output1，不行就用 output2
            problem_text = outputs.get('output1') or outputs.get('output2')
            if not problem_text:
                return jsonify({"success": False, "message": "题目生成失败（无有效输出）"}), 500

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
                "message": "题目生成成功",
                "problem": {
                    "id": problem.id,
                    "problem_text": problem_text,
                    "order": order
                }
            })
        else:
            return jsonify({"success": False, "message": "题目生成失败"}), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"生成失败: {str(e)}"}), 500

    finally:
        # 清理临时文件
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

@app.route('/api/teacher/assignments/<int:assignment_id>/submissions', methods=['GET'])
@login_required
def api_teacher_view_submissions(assignment_id):
    """查看作业提交API"""
    if not current_user.is_teacher():
        return jsonify({"success": False, "message": "无权访问"}), 403

    assignment = Assignment.query.get_or_404(assignment_id)

    if assignment.course.teacher_id != current_user.id:
        return jsonify({"success": False, "message": "无权查看此作业提交"}), 403

    # 获取所有提交的学生
    submissions = Submission.query.filter_by(assignment_id=assignment_id).all()
    
    # 获取作业的所有题目
    problems = Problem.query.filter_by(assignment_id=assignment_id).order_by(Problem.order).all()
    
    # 获取选修该课程的所有学生
    enrollments = Enrollment.query.filter_by(course_id=assignment.course_id).all()
    all_students = [enrollment.student for enrollment in enrollments]
    
    # 构建提交数据
    submissions_data = []
    submitted_student_ids = {s.student_id for s in submissions}
    
    # 已提交的学生
    for submission in submissions:
        # 获取该学生的题目提交详情
        problem_submissions = ProblemSubmission.query.filter_by(submission_id=submission.id).all()
        problem_details = []
        
        for problem in problems:
            prob_sub = next((ps for ps in problem_submissions if ps.problem_id == problem.id), None)
            problem_details.append({
                "problem_id": problem.id,
                "problem_text": problem.problem_text[:100] + "..." if len(problem.problem_text) > 100 else problem.problem_text,
                "order": problem.order,
                "answer": prob_sub.answer if prob_sub else None,
                "score": prob_sub.score if prob_sub else None,
                "grading_result": prob_sub.grading_result if prob_sub else None,
                "has_answer": bool(prob_sub and prob_sub.answer)
            })
        
        submissions_data.append({
            "id": submission.id,
            "student_id": submission.student_id,
            "student_name": submission.student.username,
            "student_email": submission.student.email,
            "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,
            "total_score": submission.total_score,
            "is_graded": submission.is_graded,
            "status": "已提交",
            "problem_count": len(problems),
            "answered_count": len([p for p in problem_details if p["has_answer"]]),
            "problems": problem_details
        })
    
    # 未提交的学生
    for student in all_students:
        if student.id not in submitted_student_ids:
            submissions_data.append({
                "id": None,
                "student_id": student.id,
                "student_name": student.username,
                "student_email": student.email,
                "submitted_at": None,
                "total_score": None,
                "is_graded": False,
                "status": "未提交",
                "problem_count": len(problems),
                "answered_count": 0,
                "problems": []
            })

    return jsonify({
        "success": True,
        "data": {
            "assignment": {
                "id": assignment.id,
                "title": assignment.title,
                "description": assignment.description,
                "course_name": assignment.course.name,
                "course_id": assignment.course_id,
                "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                "created_at": assignment.created_at.isoformat() if assignment.created_at else None,
                "problems_count": len(problems)
            },
            "problems": [
                {
                    "id": p.id,
                    "order": p.order,
                    "problem_text": p.problem_text[:100] + "..." if len(p.problem_text) > 100 else p.problem_text
                } for p in problems
            ],
            "submissions": submissions_data,
            "statistics": {
                "total_students": len(all_students),
                "submitted_count": len(submissions),
                "unsubmitted_count": len(all_students) - len(submissions),
                "submission_rate": round((len(submissions) / len(all_students)) * 100, 1) if all_students else 0,
                "graded_count": len([s for s in submissions if s.is_graded]),
                "average_score": round(sum(s.total_score for s in submissions if s.total_score is not None) / len([s for s in submissions if s.total_score is not None]), 1) if [s for s in submissions if s.total_score is not None] else None
            }
        }
    })

# ==================== 学生API ====================

@app.route('/api/student/dashboard', methods=['GET'])
@login_required
def api_student_dashboard():
    """学生仪表板API"""
    if not current_user.is_student():
        return jsonify({"success": False, "message": "无权访问"}), 403

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

            if submission and submission.submitted_at:
                completed_assignments.append({
                    'id': assignment.id,
                    'title': assignment.title,
                    'course_name': course.name,
                    'course_id': course.id,
                    'due_date': assignment.due_date.isoformat() if assignment.due_date else None,
                    'submitted_at': submission.submitted_at.isoformat() if submission.submitted_at else None,
                    'total_score': submission.total_score,
                    'is_graded': submission.is_graded
                })
            else:
                pending_assignments.append({
                    'id': assignment.id,
                    'title': assignment.title,
                    'description': assignment.description,
                    'course_name': course.name,
                    'course_id': course.id,
                    'due_date': assignment.due_date.isoformat() if assignment.due_date else None,
                    'created_at': assignment.created_at.isoformat() if assignment.created_at else None,
                    'problems_count': len(assignment.problems)
                })

    return jsonify({
        "success": True,
        "data": {
            "courses": [
                {
                    "id": c.id,
                    "name": c.name,
                    "description": c.description,
                    "teacher_name": c.teacher.username if c.teacher else "未分配",
                    "assignments_count": len(c.assignments)
                } for c in courses
            ],
            "pending_assignments": pending_assignments,
            "completed_assignments": completed_assignments,
            "stats": {
                "courses_count": len(courses),
                "pending_count": len(pending_assignments),
                "completed_count": len(completed_assignments)
            }
        }
    })

@app.route('/api/student/courses', methods=['GET'])
@login_required
def api_student_courses():
    """学生课程列表API"""
    if not current_user.is_student():
        return jsonify({"success": False, "message": "无权访问"}), 403

    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    courses = []

    for enrollment in enrollments:
        course = enrollment.course
        assignments = Assignment.query.filter_by(course_id=course.id).all()

        # 统计作业完成情况
        completed_count = 0
        for assignment in assignments:
            submission = Submission.query.filter_by(
                student_id=current_user.id,
                assignment_id=assignment.id
            ).first()
            if submission and submission.submitted_at:
                completed_count += 1

        courses.append({
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "teacher_name": course.teacher.username if course.teacher else "未分配",
            "enrollment_date": enrollment.enrolled_at.isoformat() if enrollment.enrolled_at else None,
            "assignments_total": len(assignments),
            "assignments_completed": completed_count,
            "assignments_pending": len(assignments) - completed_count
        })

    return jsonify({
        "success": True,
        "courses": courses
    })

@app.route('/api/student/assignments', methods=['GET'])
@login_required
def api_student_assignments():
    """学生作业列表API"""
    if not current_user.is_student():
        return jsonify({"success": False, "message": "无权访问"}), 403

    # 获取查询参数
    status = request.args.get('status', 'all')  # all, pending, completed
    course_id = request.args.get('course_id')

    # 获取学生选修的课程
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    course_ids = [enrollment.course_id for enrollment in enrollments]

    # 构建查询条件
    query = Assignment.query.filter(Assignment.course_id.in_(course_ids))
    if course_id:
        query = query.filter(Assignment.course_id == course_id)

    assignments = query.all()
    result = []

    for assignment in assignments:
        submission = Submission.query.filter_by(
            student_id=current_user.id,
            assignment_id=assignment.id
        ).first()

        is_completed = submission and submission.submitted_at

        # 根据状态过滤
        if status == 'pending' and is_completed:
            continue
        if status == 'completed' and not is_completed:
            continue

        assignment_data = {
            "id": assignment.id,
            "title": assignment.title,
            "description": assignment.description,
            "course_id": assignment.course_id,
            "course_name": assignment.course.name,
            "teacher_name": assignment.course.teacher.username if assignment.course.teacher else "未分配",
            "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
            "created_at": assignment.created_at.isoformat() if assignment.created_at else None,
            "problems_count": len(assignment.problems),
            "status": "completed" if is_completed else "pending"
        }

        if submission:
            assignment_data.update({
                "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,
                "total_score": submission.total_score,
                "is_graded": submission.is_graded
            })

        result.append(assignment_data)

    return jsonify({
        "success": True,
        "assignments": result
    })

@app.route('/api/student/assignments/<int:assignment_id>', methods=['GET'])
@login_required
def api_student_assignment_detail(assignment_id):
    """学生查看作业详情API"""
    if not current_user.is_student():
        return jsonify({"success": False, "message": "无权访问"}), 403

    assignment = Assignment.query.get_or_404(assignment_id)

    # 检查学生是否选修了该课程
    enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=assignment.course_id
    ).first()

    if not enrollment:
        return jsonify({"success": False, "message": "您未选修该课程"}), 403

    # 获取学生的提交
    submission = Submission.query.filter_by(
        student_id=current_user.id,
        assignment_id=assignment_id
    ).first()

    problems = Problem.query.filter_by(assignment_id=assignment_id).order_by(Problem.order).all()

    # 获取每个问题的提交情况
    problems_data = []
    for problem in problems:
        problem_data = {
            "id": problem.id,
            "problem_text": problem.problem_text,
            "reference_answer": problem.reference_answer,
            "grading_criteria": problem.grading_criteria,
            "order": problem.order
        }

        if submission:
            prob_sub = ProblemSubmission.query.filter_by(
                submission_id=submission.id,
                problem_id=problem.id
            ).first()

            if prob_sub:
                problem_data.update({
                    "answer": prob_sub.answer,
                    "score": prob_sub.score,
                    "grading_result": prob_sub.grading_result
                })

        problems_data.append(problem_data)

    result = {
        "assignment": {
            "id": assignment.id,
            "title": assignment.title,
            "description": assignment.description,
            "course_id": assignment.course_id,
            "course_name": assignment.course.name,
            "teacher_name": assignment.course.teacher.username if assignment.course.teacher else "未分配",
            "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
            "created_at": assignment.created_at.isoformat() if assignment.created_at else None
        },
        "problems": problems_data,
        "submission": None
    }

    if submission:
        result["submission"] = {
            "id": submission.id,
            "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,
            "total_score": submission.total_score,
            "is_graded": submission.is_graded
        }

    return jsonify({
        "success": True,
        "data": result
    })

@app.route('/api/student/assignments/<int:assignment_id>/submit', methods=['POST'])
@login_required
def api_student_submit_assignment(assignment_id):
    """学生提交作业API"""
    if not current_user.is_student():
        return jsonify({"success": False, "message": "无权访问"}), 403

    assignment = Assignment.query.get_or_404(assignment_id)

    # 检查学生是否选修了该课程
    enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=assignment.course_id
    ).first()

    if not enrollment:
        return jsonify({"success": False, "message": "您未选修该课程"}), 403

    data = request.get_json()
    answers = data.get('answers', {})

    if not answers:
        return jsonify({"success": False, "message": "答案不能为空"}), 400

    problems = Problem.query.filter_by(assignment_id=assignment_id).all()

    try:
        # 获取或创建提交记录
        submission = Submission.query.filter_by(
            student_id=current_user.id,
            assignment_id=assignment_id
        ).first()

        if not submission:
            submission = Submission(
                student_id=current_user.id,
                assignment_id=assignment_id,
                submitted_at=datetime.now()
            )
            db.session.add(submission)
            db.session.flush()  # 获取 submission.id
        else:
            submission.submitted_at = datetime.now()

        # 确保上传目录存在
        os.makedirs("./uploads/txt", exist_ok=True)

        # 获取API密钥用于自动评分
        api_key = os.getenv("DIFY_API_KEY_MARKING")

        # 依次保存每道题答案并进行自动评分
        for problem in problems:
            ans = answers.get(str(problem.id), "")
            if not ans.strip():
                continue

            # 获取或创建题目提交记录
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

            # 自动评分
            if api_key:
                try:
                    student_file = f"./uploads/txt/student_{problem.id}_{submission.id}.txt"
                    problem_file = f"./uploads/txt/problem_{problem.id}_{submission.id}.txt"
                    criteria_file = f"./uploads/txt/criteria_{problem.id}_{submission.id}.txt"

                    # 写入文件
                    with open(student_file, 'w', encoding='utf-8') as f:
                        f.write(ans)
                    with open(problem_file, 'w', encoding='utf-8') as f:
                        f.write(problem.problem_text)
                    with open(criteria_file, 'w', encoding='utf-8') as f:
                        f.write(problem.grading_criteria or "根据代码逻辑和功能完成度进行评分。")

                    # 调用评分API
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
                            else:
                                # 尝试其他分数格式
                                score_match = re.search(r'(\d+)分', output)
                                if score_match:
                                    score = float(score_match.group(1))
                        except:
                            score = 0

                        problem_submission.score = score
                    else:
                        problem_submission.grading_result = '自动评分失败，请等待教师手动评分'
                        problem_submission.score = 0

                    # 清理临时文件
                    for temp_file in [student_file, problem_file, criteria_file]:
                        try:
                            if os.path.exists(temp_file):
                                os.remove(temp_file)
                        except:
                            pass

                except Exception as e:
                    print(f"自动评分失败: {e}")
                    problem_submission.grading_result = '自动评分失败，请等待教师手动评分'
                    problem_submission.score = 0
            else:
                problem_submission.grading_result = '等待教师评分'
                problem_submission.score = None

        db.session.commit()

        # 更新作业总分
        api_update_submission_total_score(submission.id)

        return jsonify({
            "success": True,
            "message": "作业提交成功",
            "submission_id": submission.id
        })

    except Exception as e:
        db.session.rollback()
        print(f"提交作业失败: {e}")
        return jsonify({"success": False, "message": f"提交失败: {str(e)}"}), 500

def api_update_submission_total_score(submission_id):
    """更新作业总分的辅助函数"""
    try:
        submission = Submission.query.get(submission_id)
        if not submission:
            return

        problem_submissions = ProblemSubmission.query.filter_by(submission_id=submission_id).all()

        if not problem_submissions:
            submission.total_score = 0
            submission.is_graded = False
        else:
            # 计算总分
            total_score = 0
            graded_count = 0

            for ps in problem_submissions:
                if ps.score is not None:
                    total_score += ps.score
                    graded_count += 1

            total_problems = len(problem_submissions)

            if total_problems > 0:
                submission.total_score = total_score / total_problems
                submission.is_graded = (graded_count == total_problems)
            else:
                submission.total_score = 0
                submission.is_graded = False

        db.session.commit()

    except Exception as e:
        print(f"更新总分失败: {e}")
        db.session.rollback()

@app.route('/api/student/courses/<int:course_id>', methods=['GET'])
@login_required
def api_student_course_detail(course_id):
    """学生查看课程详情API"""
    if not current_user.is_student():
        return jsonify({"success": False, "message": "无权访问"}), 403

    # 检查学生是否选修了该课程
    enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()

    if not enrollment:
        return jsonify({"success": False, "message": "您未选修该课程"}), 403

    course = Course.query.get_or_404(course_id)

    # 获取课程作业
    assignments = Assignment.query.filter_by(course_id=course_id).all()

    # 获取作业完成情况
    assignments_data = []
    completed_count = 0
    total_score = 0
    graded_count = 0

    for assignment in assignments:
        submission = Submission.query.filter_by(
            student_id=current_user.id,
            assignment_id=assignment.id
        ).first()

        is_completed = submission and submission.submitted_at
        if is_completed:
            completed_count += 1
            if submission.is_graded and submission.total_score is not None:
                total_score += submission.total_score
                graded_count += 1

        assignment_data = {
            "id": assignment.id,
            "title": assignment.title,
            "description": assignment.description,
            "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
            "created_at": assignment.created_at.isoformat() if assignment.created_at else None,
            "problems_count": len(assignment.problems),
            "status": "completed" if is_completed else "pending"
        }

        if submission:
            assignment_data.update({
                "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,
                "total_score": submission.total_score,
                "is_graded": submission.is_graded
            })

        assignments_data.append(assignment_data)

    # 计算平均分
    average_score = total_score / graded_count if graded_count > 0 else None

    return jsonify({
        "success": True,
        "data": {
            "course": {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "teacher_name": course.teacher.username if course.teacher else "未分配",
                "enrollment_date": enrollment.enrolled_at.isoformat() if enrollment.enrolled_at else None
            },
            "assignments": assignments_data,
            "statistics": {
                "total_assignments": len(assignments),
                "completed_assignments": completed_count,
                "pending_assignments": len(assignments) - completed_count,
                "completion_rate": round((completed_count / len(assignments)) * 100, 1) if assignments else 0,
                "average_score": round(average_score, 1) if average_score is not None else None,
                "graded_assignments": graded_count
            }
        }
    })

# ==================== 智能出题和批改API ====================

@app.route('/api/run_workflow', methods=['POST'])
def api_run_workflow():
    """智能出题API"""
    # 获取API密钥
    api_key = os.getenv("DIFY_API_KEY_PROBLEM")

    # 获取上传的文件
    if 'file' not in request.files:
        return jsonify({"error": "没有上传文件"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400

    # 确保上传目录存在
    os.makedirs("./uploads/txt", exist_ok=True)

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

@app.route('/api/run_multi_workflow', methods=['POST'])
def api_run_multi_workflow():
    """智能批改API"""
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

    # 确保上传目录存在
    os.makedirs("./uploads/txt", exist_ok=True)

    # 保存文件到临时位置
    temp_path1 = "./uploads/txt/" + file1.filename
    temp_path2 = "./uploads/txt/" + file2.filename
    temp_path3 = "./uploads/txt/" + file3.filename

    file1.save(temp_path1)
    file2.save(temp_path2)
    file3.save(temp_path3)

    # 调用API
    result = run_three_txt_files_workflow(api_key, temp_path1, temp_path2, temp_path3)
    print(result)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "API调用失败"}), 500

@app.route('/api/save_generated_assignment', methods=['POST'])
@login_required
def api_save_generated_assignment():
    """保存生成的作业API"""
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
        "assignment_url": f"/teacher/assignment/{assignment.id}/edit"
    })

# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "message": "API端点不存在"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "message": "服务器内部错误"}), 500

# ==================== 健康检查 ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查API"""
    return jsonify({
        "success": True,
        "message": "API服务正常运行",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    # 确保上传目录存在
    os.makedirs("./uploads/txt", exist_ok=True)

    # 初始化数据库和管理员账号
    with app.app_context():
        create_tables()

    # 运行应用
    app.run(debug=True, port=5000)