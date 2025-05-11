
# 智能教学系统设计文档

## 1. 系统架构

### 1.1 总体架构

```
+---------------------------+
|        前端界面层          |
|  Vue(HTML/CSS/JavaScript)    |
+---------------------------+
           ↑↓
+---------------------------+
|        应用服务层          |
|    (Flask Web框架)        |
+---------------------------+
           ↑↓
+---------------------------+     +---------------------------+
|        业务逻辑层          |---->|      Dify工作流集成        |
|    (Service层)           |     | (AI自动判分/出题服务)       |
+---------------------------+     +---------------------------+
           ↑↓
+---------------------------+
|        数据访问层          |
|      (MyBatis ORM)       |
+---------------------------+
           ↑↓
+---------------------------+
|        数据存储层          |
|     (关系型数据库)         |
+---------------------------+
```

### 1.2 技术栈选型

- **前端**：Vue(HTML5, CSS3, JavaScript, Bootstrap)
- **后端**：Python Flask框架
- **ORM**：MyBatis
- **数据库**：MySQL
- **AI集成**：Dify工作流API
- **部署**：Docker容器化

## 2. 数据库设计

### 2.1 核心数据表

#### 用户表(User)
```
- id: INT (PK)
- username: VARCHAR(50)
- password: VARCHAR(128) [加密存储]
- role: ENUM('admin', 'teacher', 'student')
- email: VARCHAR(100)
- create_time: DATETIME
- update_time: DATETIME
- status: TINYINT [0-禁用, 1-启用]
```

#### 教师表(Teacher)
```
- id: INT (PK)
- user_id: INT (FK -> User.id)
- name: VARCHAR(50)
- teacher_code: VARCHAR(20) [教师编号]
- department: VARCHAR(100)
- create_time: DATETIME
- update_time: DATETIME
```

#### 学生表(Student)
```
- id: INT (PK)
- user_id: INT (FK -> User.id)
- name: VARCHAR(50)
- student_code: VARCHAR(20) [学号]
- class_name: VARCHAR(50)
- create_time: DATETIME
- update_time: DATETIME
```

#### 课程表(Course)
```
- id: INT (PK)
- name: VARCHAR(100)
- course_code: VARCHAR(20)
- description: TEXT
- credit: DECIMAL(3,1)
- create_time: DATETIME
- update_time: DATETIME
```

#### 教师-课程关联表(TeacherCourse)
```
- id: INT (PK)
- teacher_id: INT (FK -> Teacher.id)
- course_id: INT (FK -> Course.id)
- semester: VARCHAR(20) [学期]
- create_time: DATETIME
```

#### 学生-课程关联表(StudentCourse)
```
- id: INT (PK)
- student_id: INT (FK -> Student.id)
- course_id: INT (FK -> Course.id)
- semester: VARCHAR(20)
- create_time: DATETIME
```

#### 作业表(Assignment)
```
- id: INT (PK)
- title: VARCHAR(200)
- course_id: INT (FK -> Course.id)
- teacher_id: INT (FK -> Teacher.id)
- chapter: VARCHAR(50)
- difficulty: ENUM('简单', '中等', '困难')
- deadline: DATETIME
- status: ENUM('草稿', '已发布', '已截止')
- create_time: DATETIME
- update_time: DATETIME
```

#### 题目表(Question)
```
- id: INT (PK)
- assignment_id: INT (FK -> Assignment.id)
- title: VARCHAR(200)
- content: TEXT [题干]
- type: ENUM('编程题') [预留其他题型]
- difficulty: ENUM('简单', '中等', '困难')
- score: INT [分值]
- evaluation_criteria: TEXT [评判标准]
- reference_answer: TEXT [参考答案]
- order_num: INT [题目序号]
- create_time: DATETIME
- update_time: DATETIME
```

#### 学生作答表(StudentAnswer)
```
- id: INT (PK)
- student_id: INT (FK -> Student.id)
- question_id: INT (FK -> Question.id)
- answer_content: TEXT [学生代码答案]
- submit_time: DATETIME
- evaluation_result: TEXT [AI评判结果]
- score: DECIMAL(5,2) [得分]
- comments: TEXT [评语]
- status: ENUM('未提交', '已提交', '已批改')
```

### 2.2 索引设计

- User表: username(唯一索引)
- Teacher表: teacher_code(唯一索引), user_id(索引)
- Student表: student_code(唯一索引), user_id(索引)
- Course表: course_code(唯一索引)
- Assignment表: course_id + teacher_id(组合索引)
- Question表: assignment_id(索引)
- StudentAnswer表: student_id + question_id(组合唯一索引)

## 3. API接口设计

### 3.1 用户认证API

```
POST /api/auth/login
- 用途: 用户登录
- 请求参数: username, password, role
- 返回: token, user_info

POST /api/auth/logout
- 用途: 用户登出
- 请求参数: token
- 返回: success状态

GET /api/auth/profile
- 用途: 获取当前用户信息
- 请求参数: token
- 返回: user_info
```

### 3.2 管理端API

```
# 用户管理
GET /api/admin/users
POST /api/admin/users
PUT /api/admin/users/{id}
DELETE /api/admin/users/{id}

# 教师管理
GET /api/admin/teachers
POST /api/admin/teachers
PUT /api/admin/teachers/{id}
DELETE /api/admin/teachers/{id}

# 学生管理
GET /api/admin/students
POST /api/admin/students
PUT /api/admin/students/{id}
DELETE /api/admin/students/{id}

# 课程管理
GET /api/admin/courses
POST /api/admin/courses
PUT /api/admin/courses/{id}
DELETE /api/admin/courses/{id}
```

### 3.3 教师端API

```
# 课程管理
GET /api/teacher/courses
GET /api/teacher/courses/{courseId}/students

# 作业管理
GET /api/teacher/assignments
POST /api/teacher/assignments
PUT /api/teacher/assignments/{id}
DELETE /api/teacher/assignments/{id}
GET /api/teacher/assignments/overview

# 题目管理
GET /api/teacher/assignments/{assignmentId}/questions
POST /api/teacher/assignments/{assignmentId}/questions
PUT /api/teacher/questions/{id}
DELETE /api/teacher/questions/{id}
POST /api/teacher/assignments/{assignmentId}/generate-questions
    - 调用Dify工作流生成题目的接口

# 学生答题查看
GET /api/teacher/courses/{courseId}/students/{studentId}/answers
GET /api/teacher/questions/{questionId}/answers
```

### 3.4 学生端API

```
# 作业查看
GET /api/student/assignments
GET /api/student/assignments/{assignmentId}

# 答题提交
GET /api/student/questions/{questionId}
POST /api/student/questions/{questionId}/answer
    - 提交答案并调用Dify工作流进行自动评判

# 查看成绩
GET /api/student/answers
GET /api/student/answers/{answerId}
```

## 4. Dify工作流集成

### 4.1 集成架构

```
+-------------------------+     +----------------------+
|  教学系统后端服务        |---->|  Dify API 客户端     |
+-------------------------+     +----------------------+
                                          |
                                          v
                                +----------------------+
                                |  Dify 云服务/自托管  |
                                +----------------------+
                                          |
                                          v
                                +----------------------+
                                |  AI自动判分工作流    |
                                +----------------------+
```

### 4.2 主要工作流

#### 4.2.1 自动出题工作流
- 输入：课程信息、章节、难度、题型
- 输出：生成的编程题目集合，包含题干、参考答案和评判标准

#### 4.2.2 自动判分工作流
- 输入：题目信息、评判标准、学生答案
- 输出：评分结果、详细评语、改进建议

### 4.3 API调用示例

```python
def submit_for_evaluation(question_content, evaluation_criteria, student_answer):
    """
    提交学生答案到Dify工作流进行自动评判
    """
    # 配置API密钥和端点
    API_KEY = "app-xxxxxxxxxxxxxxxx"
    API_URL = "https://api.dify.ai/v1/workflows/run"
    
    # 构建请求
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 输入参数
    data = {
        "inputs": {
            "Question": question_content,
            "Evaluate_standard": evaluation_criteria,
            "Student_answer": student_answer
        },
        "response_mode": "blocking",
        "user": f"student-{student_id}"
    }
    
    # 发送请求
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return {
            "score": extract_score(result),
            "feedback": extract_feedback(result),
            "suggestions": extract_suggestions(result)
        }
    else:
        # 处理错误情况
        return {"error": "评判服务暂时不可用"}
```

## 5. 部署方案

### 5.1 开发环境部署
- 本地开发：使用Docker Compose搭建开发环境
- 版本控制：Git仓库管理代码
- 数据库：开发环境使用Docker容器化MySQL
- Dify服务：开发阶段可使用Dify云服务或本地部署版

### 5.2 生产环境部署
- 服务器：云服务器(推荐2核4G以上配置)
- 容器化：使用Docker管理所有服务组件
- 数据库：独立MySQL服务或云数据库服务
- HTTPS：使用Nginx配置SSL证书
- 备份策略：数据库每日自动备份

### 5.3 容器组织
```
- nginx-container: 前端静态资源+反向代理
- flask-app-container: Flask后端应用
- mysql-container: 数据库服务
- dify-container: 可选的本地Dify服务(如不使用云服务)
```

## 6. 安全性设计

### 6.1 身份认证与授权
- JWT令牌认证机制
- 基于角色的权限控制(RBAC)
- 密码强度要求和加盐哈希存储

### 6.2 数据安全
- 所有HTTP请求使用HTTPS加密
- 敏感信息(如API密钥)使用环境变量管理
- 数据库定期备份

### 6.3 防护措施
- 防SQL注入：参数化查询
- 防XSS攻击：输入验证和输出编码
- 防CSRF攻击：使用CSRF令牌
- 请求限速：防止暴力破解和DoS攻击

## 7. 系统监控与日志

### 7.1 日志系统
- 应用日志：Flask应用日志
- 系统日志：服务器和Docker日志
- 审计日志：关键操作记录

### 7.2 监控指标
- 系统健康状态
- API响应时间
- Dify工作流调用成功率
- 数据库性能指标

### 7.3 告警机制
- 邮件/短信告警
- 关键服务不可用告警
- API调用异常告警

## 8. 扩展性考虑

### 8.1 未来功能扩展
- 支持更多题型：选择题、填空题、论述题等
- 学生作业统计分析功能
- 集成在线IDE环境
- 支持代码运行和测试

### 8.2 技术扩展性
- 微服务架构演进准备
- API版本控制
- 缓存层引入
- 负载均衡

---

这份完善的系统设计文档提供了智能教学系统的整体架构、数据模型、API设计、Dify集成方案和部署策略。系统采用现代化的架构设计，通过与Dify工作流的无缝集成，实现了编程作业的智能出题和自动批改功能，大大提高了教学效率和学习体验。
