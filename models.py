from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# 用户角色
class Role:
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'

# 用户模型
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    courses_teaching = db.relationship('Course', backref='teacher', lazy=True, foreign_keys='Course.teacher_id')
    courses_enrolled = db.relationship('Enrollment', back_populates='student', lazy=True)
    submissions = db.relationship('Submission', backref='student', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == Role.ADMIN
    
    def is_teacher(self):
        return self.role == Role.TEACHER
    
    def is_student(self):
        return self.role == Role.STUDENT

# 课程模型
class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    enrollments = db.relationship('Enrollment', back_populates='course', lazy=True)
    assignments = db.relationship('Assignment', backref='course', lazy=True)

# 选课关系模型
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    student = db.relationship('User', back_populates='courses_enrolled')
    course = db.relationship('Course', back_populates='enrollments')
    
    # 复合唯一索引确保一个学生只能选修一门课程一次
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='_student_course_uc'),)

# 作业模型
class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    
    # 关系
    problems = db.relationship('Problem', backref='assignment', lazy=True)
    submissions = db.relationship('Submission', backref='assignment', lazy=True)

# 题目模型
class Problem(db.Model):
    __tablename__ = 'problems'
    
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    problem_text = db.Column(db.Text, nullable=False)  # 题目内容
    reference_answer = db.Column(db.Text, nullable=True)  # 参考答案
    grading_criteria = db.Column(db.Text, nullable=True)  # 评分标准
    order = db.Column(db.Integer, default=0)  # 题目顺序
    
    # 关系
    submissions = db.relationship('ProblemSubmission', backref='problem', lazy=True)

# 学生提交作业模型
class Submission(db.Model):
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_graded = db.Column(db.Boolean, default=False)
    total_score = db.Column(db.Float, nullable=True)
    
    # 关系
    problem_submissions = db.relationship('ProblemSubmission', backref='submission', lazy=True)
    
    # 复合唯一索引确保一个学生只能提交一次作业
    __table_args__ = (db.UniqueConstraint('student_id', 'assignment_id', name='_student_assignment_uc'),)

# 单个题目的提交记录
class ProblemSubmission(db.Model):
    __tablename__ = 'problem_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    answer = db.Column(db.Text, nullable=True)  # 学生答案
    grading_result = db.Column(db.Text, nullable=True)  # 评分结果，JSON格式
    score = db.Column(db.Float, nullable=True)  # 得分
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 复合唯一索引确保一个题目只能提交一次
    __table_args__ = (db.UniqueConstraint('submission_id', 'problem_id', name='_submission_problem_uc'),) 