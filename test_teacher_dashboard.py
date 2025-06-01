#!/usr/bin/env python3
"""
教师Dashboard API测试脚本
用于验证前后端通信是否正常
"""

import requests
import json
import sys
from datetime import datetime

# API基础URL
BASE_URL = "http://127.0.0.1:5000/api"

# 测试用户凭据
TEST_CREDENTIALS = {
    "username": "teacher",
    "password": "teacher"
}

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def test_health(self):
        """测试API健康状态"""
        print("🔍 测试API健康状态...")
        try:
            response = self.session.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ API服务器正常运行")
                return True
            else:
                print(f"❌ API服务器响应异常: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到API服务器，请确保后端服务已启动")
            return False
        except Exception as e:
            print(f"❌ 健康检查失败: {e}")
            return False
    
    def login(self):
        """测试登录功能"""
        print("🔐 测试教师登录...")
        try:
            response = self.session.post(
                f"{BASE_URL}/auth/login",
                json=TEST_CREDENTIALS
            )
            data = response.json()
            
            if data.get('success'):
                user = data.get('user', {})
                print(f"✅ 登录成功: {user.get('username')} ({user.get('role')})")
                return True
            else:
                print(f"❌ 登录失败: {data.get('message')}")
                return False
        except Exception as e:
            print(f"❌ 登录请求失败: {e}")
            return False
    
    def test_current_user(self):
        """测试获取当前用户信息"""
        print("👤 测试获取当前用户信息...")
        try:
            response = self.session.get(f"{BASE_URL}/auth/current")
            data = response.json()
            
            if data.get('success'):
                user = data.get('user', {})
                print(f"✅ 用户信息获取成功: {user.get('username')}")
                print(f"   角色: {user.get('role')}")
                print(f"   邮箱: {user.get('email')}")
                return True
            else:
                print(f"❌ 获取用户信息失败: {data.get('message')}")
                return False
        except Exception as e:
            print(f"❌ 用户信息请求失败: {e}")
            return False
    
    def test_teacher_dashboard(self):
        """测试教师仪表板API"""
        print("📊 测试教师仪表板API...")
        try:
            response = self.session.get(f"{BASE_URL}/teacher/dashboard")
            data = response.json()
            
            if data.get('success'):
                dashboard_data = data.get('data', {})
                courses = dashboard_data.get('courses', [])
                assignments = dashboard_data.get('assignments', [])
                stats = dashboard_data.get('stats', {})
                
                print("✅ 仪表板数据获取成功:")
                print(f"   课程数量: {len(courses)}")
                print(f"   作业数量: {len(assignments)}")
                print(f"   统计信息: {stats}")
                
                # 显示课程详情
                if courses:
                    print("   课程列表:")
                    for course in courses:
                        print(f"     - {course.get('name')}: {course.get('students_count')}名学生, {course.get('assignments_count')}个作业")
                
                # 显示作业详情
                if assignments:
                    print("   最近作业:")
                    for assignment in assignments[:3]:  # 只显示前3个
                        print(f"     - {assignment.get('title')} ({assignment.get('course')})")
                
                return True
            else:
                print(f"❌ 仪表板数据获取失败: {data.get('message')}")
                return False
        except Exception as e:
            print(f"❌ 仪表板请求失败: {e}")
            return False
    
    def test_teacher_courses(self):
        """测试教师课程列表API"""
        print("📚 测试教师课程列表API...")
        try:
            response = self.session.get(f"{BASE_URL}/teacher/courses")
            data = response.json()
            
            if data.get('success'):
                courses = data.get('courses', [])
                print(f"✅ 课程列表获取成功: {len(courses)}门课程")
                
                for course in courses:
                    print(f"   - {course.get('name')}: {course.get('description')}")
                
                return True
            else:
                print(f"❌ 课程列表获取失败: {data.get('message')}")
                return False
        except Exception as e:
            print(f"❌ 课程列表请求失败: {e}")
            return False
    
    def logout(self):
        """测试登出功能"""
        print("🚪 测试登出...")
        try:
            response = self.session.post(f"{BASE_URL}/auth/logout")
            data = response.json()
            
            if data.get('success'):
                print("✅ 登出成功")
                return True
            else:
                print(f"❌ 登出失败: {data.get('message')}")
                return False
        except Exception as e:
            print(f"❌ 登出请求失败: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🧪 开始教师Dashboard API测试")
        print("=" * 50)
        
        tests = [
            ("API健康检查", self.test_health),
            ("教师登录", self.login),
            ("获取当前用户", self.test_current_user),
            ("教师仪表板", self.test_teacher_dashboard),
            ("教师课程列表", self.test_teacher_courses),
            ("用户登出", self.logout)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔬 {test_name}...")
            if test_func():
                passed += 1
            print("-" * 30)
        
        print(f"\n📈 测试结果: {passed}/{total} 项测试通过")
        
        if passed == total:
            print("🎉 所有测试通过! 前后端通信正常")
            return True
        else:
            print("⚠️  部分测试失败，请检查后端服务和数据库")
            return False

def main():
    print("🚀 智能教学系统 - 教师Dashboard API测试")
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tester = APITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ 测试完成! 可以启动前端进行测试")
        print("💡 提示: 运行 'cd vue-app && npm run dev' 启动前端服务")
    else:
        print("\n❌ 测试失败! 请检查:")
        print("   1. 后端服务是否已启动 (python api_app.py)")
        print("   2. 数据库是否已初始化")
        print("   3. 测试用户teacher/teacher是否存在")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 