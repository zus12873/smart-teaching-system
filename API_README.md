# 智能教学系统 API 文档

## 🏗️ 架构说明

本项目采用前后端分离架构：

- **前端**: Vue 3 + Vite + Bootstrap 5 (端口: 5174)
- **后端**: Flask API (端口: 5000)
- **数据库**: SQLite

## 🚀 快速启动

### 方法一：使用启动脚本（推荐）

```bash
# 给脚本执行权限
chmod +x start_dev.sh

# 启动开发环境
./start_dev.sh
```

### 方法二：手动启动

1. **启动API后端**
```bash
# 安装依赖
pip install flask-cors

# 启动API服务器
python api_app.py
```

2. **启动Vue前端**
```bash
cd vue-app
npm run dev
```

## 📍 访问地址

- **前端应用**: http://localhost:5174
- **API后端**: http://localhost:5000/api
- **API健康检查**: http://localhost:5000/api/health

## 🔑 默认账号

- **管理员账号**: admin / admin

## 🎯 主要功能页面

- **首页**: http://localhost:5174/
- **智能出题**: http://localhost:5174/problem-generation
- **智能批改**: http://localhost:5174/multi-upload
- **管理面板**: http://localhost:5174/admin/dashboard
- **用户管理**: http://localhost:5174/admin/users
- **课程管理**: http://localhost:5174/admin/courses

## 📚 API 端点

### 认证相关
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `GET /api/auth/current` - 获取当前用户信息

### 管理员功能
- `GET /api/admin/dashboard` - 获取仪表板数据
- `GET /api/admin/users` - 获取用户列表
- `POST /api/admin/users` - 创建用户
- `GET /api/admin/users/{id}` - 获取用户详情
- `PUT /api/admin/users/{id}` - 更新用户信息
- `DELETE /api/admin/users/{id}` - 删除用户
- `GET /api/admin/courses` - 获取课程列表
- `POST /api/admin/courses` - 创建课程
- `GET /api/admin/courses/{id}` - 获取课程详情
- `PUT /api/admin/courses/{id}` - 更新课程信息
- `DELETE /api/admin/courses/{id}` - 删除课程

### 智能功能
- `POST /api/run_workflow` - 智能出题
- `POST /api/run_multi_workflow` - 智能批改
- `GET /api/teacher_courses_api` - 获取教师课程列表
- `POST /api/save_generated_assignment` - 保存生成的作业

### 系统功能
- `GET /api/health` - 健康检查

## 🔧 技术栈

### 后端 (api_app.py)
- **Flask**: Web框架
- **Flask-CORS**: 跨域支持
- **Flask-Login**: 用户认证
- **SQLAlchemy**: ORM
- **Werkzeug**: 密码加密

### 前端 (vue-app/)
- **Vue 3**: 前端框架
- **Vite**: 构建工具
- **Vue Router**: 路由管理
- **Axios**: HTTP客户端
- **Bootstrap 5**: UI框架
- **Bootstrap Icons**: 图标库

## 📁 项目结构

```
smart-teaching-system/
├── api_app.py              # API后端服务器
├── app.py                  # 原始Flask应用（保留）
├── models.py               # 数据模型
├── workflow_utils.py       # AI工作流工具
├── start_dev.sh           # 开发环境启动脚本
├── vue-app/               # Vue前端项目
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── utils/         # 工具类
│   │   ├── router/        # 路由配置
│   │   └── main.js        # 入口文件
│   ├── package.json       # 前端依赖
│   └── vite.config.js     # Vite配置
├── templates/             # 原始模板（保留）
├── uploads/               # 文件上传目录
└── requirements.txt       # Python依赖
```

## 🔄 API 响应格式

### 成功响应
```json
{
  "success": true,
  "message": "操作成功",
  "data": {
    // 具体数据
  }
}
```

### 错误响应
```json
{
  "success": false,
  "message": "错误信息"
}
```

## 🛠️ 开发说明

### 添加新的API端点

1. 在 `api_app.py` 中添加路由函数
2. 在 `vue-app/src/utils/api.js` 中添加对应的API方法
3. 在Vue组件中调用API方法

### 前端组件开发

1. 在 `vue-app/src/views/` 中创建新组件
2. 在 `vue-app/src/router/index.js` 中添加路由
3. 使用 `vue-app/src/utils/api.js` 中的API方法

### 数据库模型

数据模型定义在 `models.py` 中，包括：
- User（用户）
- Course（课程）
- Assignment（作业）
- Problem（题目）
- Submission（提交）
- Enrollment（选课）

## 🔒 安全说明

- 使用Flask-Login进行会话管理
- 密码使用Werkzeug进行哈希加密
- API支持CORS但限制了凭据传递
- 所有管理员操作都需要权限验证

## 🐛 故障排除

### 常见问题

1. **CORS错误**: 确保API后端已启动且配置了CORS
2. **端口冲突**: 检查5000和5174端口是否被占用
3. **依赖缺失**: 运行 `pip install flask-cors` 安装缺失依赖
4. **数据库错误**: 删除 `teaching_system.db` 重新初始化

### 日志查看

- API后端日志会在终端显示
- Vue前端日志在浏览器开发者工具中查看

## 📞 支持

如有问题，请检查：
1. 所有依赖是否正确安装
2. 端口是否被占用
3. 环境变量是否正确配置
4. 数据库文件是否存在且可访问 