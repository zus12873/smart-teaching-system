#!/usr/bin/env python3
"""
测试教师课程API
"""

import requests
import json

# API基础URL  
BASE_URL = "http://127.0.0.1:5000/api"

def test_teacher_courses_api():
    """测试教师课程API"""
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    print("🔐 登录教师用户...")
    
    # 先登录
    login_data = {
        "username": "Mr.X",
        "password": "password"  # 请根据实际密码修改
    }
    
    try:
        login_response = session.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"登录响应状态码: {login_response.status_code}")
        print(f"登录响应内容: {login_response.text}")
        
        if login_response.status_code == 200:
            print("✅ 登录成功")
            
            # 测试获取课程列表
            print("\n📚 测试获取课程列表...")
            courses_response = session.get(f"{BASE_URL}/teacher/courses")
            print(f"课程列表响应状态码: {courses_response.status_code}")
            print(f"课程列表响应内容: {courses_response.text}")
            
            if courses_response.status_code == 200:
                courses_data = courses_response.json()
                if courses_data.get('success'):
                    courses = courses_data.get('courses', [])
                    print(f"✅ 获取到 {len(courses)} 个课程")
                    for course in courses:
                        print(f"  - {course.get('name')} (ID: {course.get('id')})")
                else:
                    print(f"❌ API返回错误: {courses_data.get('message')}")
            else:
                print(f"❌ 获取课程列表失败，状态码: {courses_response.status_code}")
        else:
            print("❌ 登录失败")
            # 尝试使用默认密码
            login_data["password"] = "teacher"
            login_response = session.post(f"{BASE_URL}/auth/login", json=login_data)
            print(f"使用默认密码登录状态码: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("✅ 使用默认密码登录成功")
                
                # 测试获取课程列表
                print("\n📚 测试获取课程列表...")
                courses_response = session.get(f"{BASE_URL}/teacher/courses")
                print(f"课程列表响应状态码: {courses_response.status_code}")
                print(f"课程列表响应内容: {courses_response.text}")
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

if __name__ == "__main__":
    test_teacher_courses_api() 