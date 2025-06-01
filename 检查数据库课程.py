#!/usr/bin/env python3
"""
检查数据库中的课程数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_app import app, db, User, Course, Role
from sqlalchemy import text

def check_database():
    with app.app_context():
        print("🔍 检查数据库中的数据...")
        
        # 检查用户
        print("\n👥 用户列表:")
        users = User.query.all()
        for user in users:
            print(f"  - {user.username} ({user.role}) - ID: {user.id}")
        
        # 检查课程
        print("\n📚 课程列表:")
        courses = Course.query.all()
        if not courses:
            print("  暂无课程数据")
            
            # 创建测试课程数据
            print("\n📝 创建测试课程数据...")
            teacher = User.query.filter_by(role=Role.TEACHER).first()
            if teacher:
                test_courses = [
                    {
                        'name': '计算机基础',
                        'description': '计算机科学基础知识学习',
                        'teacher_id': teacher.id
                    },
                    {
                        'name': 'Python编程',
                        'description': 'Python语言程序设计课程',
                        'teacher_id': teacher.id
                    },
                    {
                        'name': '数据结构与算法',
                        'description': '数据结构和算法设计与分析',
                        'teacher_id': teacher.id
                    }
                ]
                
                for course_data in test_courses:
                    course = Course(**course_data)
                    db.session.add(course)
                
                db.session.commit()
                print("✅ 测试课程数据创建成功!")
                
                # 重新查询课程
                courses = Course.query.all()
            else:
                print("❌ 没有找到教师用户，无法创建课程")
        
        for course in courses:
            teacher_name = course.teacher.username if course.teacher else "未分配"
            print(f"  - {course.name}: {course.description} (教师: {teacher_name}) - ID: {course.id}")
        
        # 检查教师课程关联
        print("\n🔗 教师课程关联:")
        teachers = User.query.filter_by(role=Role.TEACHER).all()
        for teacher in teachers:
            teacher_courses = Course.query.filter_by(teacher_id=teacher.id).all()
            print(f"  教师 {teacher.username} 负责的课程:")
            if teacher_courses:
                for course in teacher_courses:
                    print(f"    - {course.name} (ID: {course.id})")
            else:
                print("    暂无负责的课程")

if __name__ == "__main__":
    check_database() 