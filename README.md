# 智能教学系统 🎓

基于 Flask + Vue.js + AI 的现代化智能教学平台，集成智能出题和自动评分功能。

## 📋 项目概述

智能教学系统是一个面向教师和学生的现代化教学平台，采用前后端分离架构，提供完整的在线教学解决方案。

### 🌟 主要特性

- **🤖 智能出题**：利用AI自动生成各类型题目，支持从题库抽取或全新生成
- **🎯 智能批改**：利用AI自动评阅学生提交的作业，提供详细的评分和反馈
- **👥 用户管理**：支持管理员、教师和学生三种角色，权限分明
- **📚 课程管理**：教师可创建课程、管理作业，学生可选课、完成作业
- **📊 学习分析**：提供学习数据分析，帮助教师了解学生学习情况
- **💻 现代化UI**：Vue.js + Bootstrap 5 打造的响应式前端界面
- **🔄 前后端分离**：Flask API + Vue.js SPA，易于维护和扩展

### 🏗️ 技术架构

**后端技术栈：**
- Python 3.9+
- Flask 3.0+ (Web框架)
- SQLAlchemy (ORM)
- SQLite/MySQL/PostgreSQL (数据库)
- Dify API (AI服务)
- Flask-Login (用户认证)

**前端技术栈：**
- Vue.js 3 (渐进式框架)
- Vite (构建工具)
- Vue Router (路由管理)
- Axios (HTTP客户端)
- Bootstrap 5 (UI框架)
- Chart.js (图表库)

## 🚀 快速开始

### 📋 环境要求

- **Node.js** 16.0+
- **Python** 3.9+
- **Git**

### 📥 项目克隆

```bash
git clone https://github.com/zus12873/smart-teaching-system.git
cd smart-teaching-system
```

## 🔧 后端部署 (Flask API)

### 1. 创建Python虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 3. 环境变量配置

在项目根目录创建 `.env` 文件：

```env

# AI服务配置 (可选)
DIFY_API_KEY_PROBLEM=''#题目生成api
DIFY_API_KEY_MARKING=''#评分api
DIFY_BASE_URL='https://api.dify.ai'
```

### 4. 初始化数据库

app.py/api_app.py初次运行时会生成`.db`文件

### 5. 启动后端服务

```bash
# 开发模式启动
python app.py#前后端耦合的系统
python api_app.py#前后端分离的flask API文件

```

前后端耦合系统的服务将在 `http://127.0.0.1:5001` 启动
前后端分离的系统在`http://127.0.0.1:5000`启动
**默认管理员账户：**
- 用户名: `admin`
- 密码: `admin`

## 🎨 前端部署 (Vue.js)

### 1. 进入前端目录

```bash
cd vue-app
```

### 2. 安装Node.js依赖
先在对应的系统中安装npm环境
```bash
npm install
```

### 3. 启动开发服务器

```bash
npm run dev
```

前端应用将在 `http://localhost:5173` 启动

### 4. 构建生产版本

```bash
npm run build
```

构建后的文件将生成在 `vue-app/dist/` 目录中。

## 🌐 完整系统启动

### 开发环境

1. **启动后端服务**（终端1）：
```bash
# 激活Python虚拟环境
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 启动前后端耦合的Flask应用
python app.py
# 启动前后端分离的Flask后端 API
python api_app.py
```

2. **启动前端服务**（终端2）：
```bash
cd vue-app
npm run dev
```

3. **访问应用**：
- 前端界面: `http://localhost:5173`
- 后端API: `http://127.0.0.1:5000`

### 生产环境

1. **构建前端**：
```bash
cd vue-app
npm run build
```

2. **部署配置**：
可以使用 Nginx 代理前端静态文件和后端API，或者使用其他web服务器。

## 📚 系统功能说明

### 👨‍💼 管理员功能

- **用户管理**：创建和管理教师和学生账户
- **课程管理**：创建课程并分配给教师
- **系统监控**：查看系统整体使用数据

### 👨‍🏫 教师功能

- **课程管理**：查看负责的课程，管理选课学生
- **作业管理**：创建作业，添加题目，查看学生提交
- **智能出题**：使用AI自动生成题目，或从题库中抽取题目
- **智能批改**：使用AI自动评阅学生提交的答案

### 👨‍🎓 学生功能

- **课程查看**：查看已选修的课程
- **作业完成**：查看、完成和提交作业
- **成绩查询**：查看作业评分和反馈
- **学习分析**：查看个人学习数据和统计

## 🤖 AI功能配置

系统集成了基于 Dify API 的两个主要AI功能：

### 智能出题

- 支持根据指定条件自动生成题目
- 可从题库文件中抽取相关题目
- 支持多种题型：编程题、选择题等

### 智能批改

- 自动评阅学生提交的作业
- 提供详细的评分和反馈
- 支持教师手动修改评分结果

要启用AI功能，请在 `.env` 文件中配置相应的API密钥。

## 📁 项目结构

```
smart-teaching-system/
├── vue-app/                 # Vue.js前端应用
│   ├── src/
│   │   ├── components/      # Vue组件
│   │   ├── views/          # 页面视图
│   │   ├── router/         # 路由配置
│   │   ├── stores/         # 状态管理
│   │   └── utils/          # 工具函数
│   ├── public/             # 静态资源
│   ├── package.json        # Node.js依赖
│   └── vite.config.js      # Vite配置
├── templates/              # Flask模板（传统模式）
├── upload_files/           # 文件上传目录
├── workflow_configs/       # AI工作流配置
├── app.py                  # Flask主应用
├── api_app.py              # API应用
├── models.py               # 数据模型
├── workflow_utils.py       # AI工作流工具
├── requirements.txt        # Python依赖
└── .env                    # 环境变量配置
```

## 🔧 开发指南

### API接口

后端提供RESTful API接口，主要端点包括：

- `/api/teacher/courses` - 教师课程管理
- `/api/save_generated_assignment` - 保存生成的作业
- `/run_workflow` - 运行AI工作流
- `/run_multi_workflow` - 运行多文件工作流

### 数据库

使用SQLAlchemy ORM管理数据库，主要模型：

- `User` - 用户模型
- `Course` - 课程模型
- `Assignment` - 作业模型
- `Problem` - 题目模型
- `Submission` - 提交模型

### 前端代理配置

前端开发服务器配置了代理，将 `/api` 请求转发到后端服务器：

```javascript
// vite.config.js
proxy: {
  '/api': {
    target: 'http://127.0.0.1:5000',
    changeOrigin: true
  }
}
```

## 🐛 故障排除

### 常见问题

1. **后端启动失败**
   - 检查Python版本是否>=3.9
   - 确认已激活虚拟环境
   - 检查端口5000是否被占用

2. **前端启动失败**
   - 检查Node.js版本是否>=16.0
   - 删除 `node_modules` 重新安装依赖
   - 检查端口5173是否被占用

3. **数据库连接错误**
   - 检查 `.env` 文件中的数据库配置
   - 确认数据库文件权限

4. **AI功能不可用**
   - 检查API密钥配置
   - 确认网络连接

## 🤝 贡献指南

欢迎贡献代码或提出建议：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 📞 联系方式

如有任何问题或建议，请联系项目维护者：

- **GitHub Issues**: [Issues页面](https://github.com/zus12873/smart-teaching-system/issues)
- **邮箱**: zcx12873@gmail.com

---

**快速启动提醒**: 首次部署请确保同时启动后端和前端服务，并使用默认管理员账户 `admin/admin` 登录系统进行初始配置。 