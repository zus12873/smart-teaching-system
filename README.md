# 智能教学系统

基于Flask和AI的现代化智能教学平台，集成智能出题和自动评分功能。

## 系统概述

智能教学系统是一个面向教师和学生的现代化教学平台，主要功能包括：

- **智能出题**：利用AI自动生成各类型题目，支持从题库抽取或全新生成
- **智能批改**：利用AI自动评阅学生提交的作业，提供详细的评分和反馈
- **用户管理**：支持管理员、教师和学生三种角色，不同权限分明
- **课程管理**：教师可创建课程、管理作业，学生可选课、完成作业
- **学习分析**：提供学习数据分析，帮助教师了解学生学习情况

## 安装与设置

### 环境要求

- Python 3.9+
- Flask 3.0+
- SQLAlchemy
- 其他依赖项见 requirements.txt

### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/yourusername/smart-teaching-system.git
cd smart-teaching-system
```

2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置环境变量

创建 `.env` 文件并添加以下内容：

```
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///teaching_system.db
DIFY_API_KEY_PROBLEM=your_dify_problem_api_key
DIFY_API_KEY_MARKING=your_dify_marking_api_key
```

5. 初始化数据库

```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

6. 运行应用

```bash
flask run
```

访问 http://127.0.0.1:5000 即可使用系统。

## 主要功能

### 管理员功能

- 用户管理：创建和管理教师和学生账户
- 课程管理：创建课程并分配给教师
- 系统监控：查看系统整体使用数据

### 教师功能

- 课程管理：查看负责的课程，管理选课学生
- 作业管理：创建作业，添加题目，查看学生提交
- 智能出题：使用AI自动生成题目，或从题库中抽取题目
- 智能批改：使用AI自动评阅学生提交的答案

### 学生功能

- 课程查看：查看已选修的课程
- 作业完成：查看、完成和提交作业
- 成绩查询：查看作业评分和反馈
- 学习分析：查看个人学习数据和统计

## AI功能说明

本系统集成了两个主要的AI功能，它们基于Dify API实现：

### 智能出题

系统可以根据指定的学科、难度等条件，自动生成各类型题目，包括编程题、选择题等。您可以：

- 上传题库文件，AI会从中抽取相关题目
- 直接指定条件，AI会全新生成题目
- 支持设置题目难度、类型和数量

### 智能批改

系统可以自动评阅学生提交的作业，特别是编程类作业，提供详细的评分和反馈：

- 上传学生答案、标准题目和评分标准
- AI会对照评分标准给出分数和具体反馈
- 支持教师手动修改评分结果

## 使用流程

### 教师流程

1. 登录系统
2. 查看已分配的课程
3. 创建新作业
4. 使用智能出题生成题目或手动添加题目
5. 发布作业
6. 查看学生提交情况
7. 查看AI自动评分或手动批改

### 学生流程

1. 登录系统
2. 查看已选修的课程和作业
3. 进入作业页面完成题目
4. 提交答案接受AI自动评分
5. 查看评分结果和反馈
6. 查看个人学习分析数据

## 技术架构

- 前端：HTML, CSS, JavaScript, Bootstrap 5
- 后端：Python, Flask
- 数据库：SQLite (可扩展至MySQL或PostgreSQL)
- AI服务：Dify API
- 部署：可部署于传统服务器或容器环境

## 贡献指南

欢迎贡献代码或提出建议，请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 联系方式

如有任何问题或建议，请联系项目维护者：

- 电子邮件：your.email@example.com
- GitHub Issues：https://github.com/yourusername/smart-teaching-system/issues 