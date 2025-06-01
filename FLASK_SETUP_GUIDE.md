# 智能教学系统 Flask 后端环境配置指南

## 📋 系统要求

- **Python**: 3.8.0 或更高版本（推荐 3.9+ 或 3.10+）
- **pip**: Python 包管理器
- **Git**: 用于克隆项目
- **操作系统**: Windows 10+、macOS 10.15+、Ubuntu 18.04+

## 🚀 快速开始

### 1. 安装 Python

#### Windows 系统
1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载 Python 3.9+ 版本
3. 运行安装包，**务必勾选 "Add Python to PATH"**
4. 验证安装：
```bash
python --version
pip --version
```

#### macOS 系统
```bash
# 使用 Homebrew 安装（推荐）
brew install python

# 验证安装
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian) 系统
```bash
# 更新包管理器
sudo apt update

# 安装 Python 和 pip
sudo apt install python3 python3-pip python3-venv

# 验证安装
python3 --version
pip3 --version
```

### 2. 克隆项目

```bash
# 克隆项目到本地
git clone <your-repository-url>
cd smart-teaching-system

# 或者如果已有项目文件，直接进入目录
cd smart-teaching-system
```

### 3. 创建虚拟环境

```bash
# 在项目根目录创建虚拟环境
python -m venv venv

# 或者在 Linux/macOS 上
python3 -m venv venv
```

### 4. 激活虚拟环境

#### Windows 系统
```bash
# 命令提示符
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1

# Git Bash
source venv/Scripts/activate
```

#### macOS/Linux 系统
```bash
source venv/bin/activate
```

激活成功后，命令行前面会显示 `(venv)`

### 5. 安装依赖

```bash
# 确保虚拟环境已激活
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 如果 requirements.txt 不存在，手动安装主要依赖
pip install flask flask-sqlalchemy flask-login flask-cors python-dotenv requests
```

### 6. 配置环境变量

在项目根目录创建 `.env` 文件：

```bash
# .env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/database.db
DIFY_API_KEY=your-dify-api-key
DIFY_API_URL=https://api.dify.ai/v1
```

### 7. 初始化数据库

```bash
# 在项目根目录运行
python app.py

# 首次运行会自动创建数据库表
```

### 8. 启动 Flask 服务器

```bash
# 方法1：直接运行
python app.py

# 方法2：使用 flask 命令
flask run

# 方法3：使用提供的启动脚本
chmod +x start_dev.sh  # Linux/macOS
./start_dev.sh

# Windows
start_dev.bat
```

服务器将在 http://127.0.0.1:5000 启动

## 🔧 详细配置说明

### 项目依赖说明

根据 `requirements.txt` 文件，主要依赖包括：

#### 核心框架
- **Flask**: Web 框架
- **Flask-SQLAlchemy**: ORM 数据库工具
- **Flask-Login**: 用户认证管理
- **Flask-CORS**: 跨域资源共享

#### 数据处理
- **requests**: HTTP 请求库
- **python-dotenv**: 环境变量管理
- **Werkzeug**: WSGI 工具库

### 数据库配置

项目使用 SQLite 数据库，数据库文件位于 `instance/` 目录：

```python
# models.py 中的配置
SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### API 配置

项目集成了 Dify AI 服务，需要在 `.env` 文件中配置：

```bash
DIFY_API_KEY=your-dify-api-key
DIFY_API_URL=https://api.dify.ai/v1
```

## 🛠️ 常用命令

```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 退出虚拟环境
deactivate

# 安装新依赖
pip install <package-name>

# 更新 requirements.txt
pip freeze > requirements.txt

# 运行应用
python app.py

# 调试模式运行
export FLASK_DEBUG=1  # Linux/macOS
set FLASK_DEBUG=1     # Windows
python app.py
```

## 🐛 常见问题解决

### 1. Python 版本问题
```bash
# 检查 Python 版本
python --version

# 如果系统有多个 Python 版本
python3 --version
python3.9 --version

# 使用特定版本创建虚拟环境
python3.9 -m venv venv
```

### 2. 虚拟环境问题
```bash
# 删除虚拟环境重新创建
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# 重新创建
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. 依赖安装失败
```bash
# 升级 pip
pip install --upgrade pip

# 清理 pip 缓存
pip cache purge

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 4. 端口占用问题
```bash
# 查看端口占用 (5000)
# Linux/macOS
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# 或者修改端口
# 在 app.py 中: app.run(host='0.0.0.0', port=8000, debug=True)
```

### 5. 权限问题（Linux/macOS）
```bash
# 如果遇到权限问题
sudo chown -R $(whoami) ./
chmod +x start_dev.sh
```

### 6. 数据库问题
```bash
# 删除数据库重新创建
rm instance/database.db
python app.py  # 重新创建数据库表
```

## 📁 项目结构

```
smart-teaching-system/
├── app.py                 # 主应用文件
├── api_app.py            # API 应用文件
├── models.py             # 数据库模型
├── workflow_utils.py     # 工作流工具
├── requirements.txt      # Python 依赖
├── .env                  # 环境变量
├── instance/            # 数据库文件目录
├── uploads/             # 文件上传目录
├── templates/           # HTML 模板
├── vue-app/             # Vue 前端
└── venv/                # 虚拟环境
```

## 🔄 项目更新

当项目有更新时：

```bash
# 拉取最新代码
git pull origin main

# 激活虚拟环境
source venv/bin/activate

# 更新依赖（如果 requirements.txt 有变化）
pip install -r requirements.txt

# 重启服务器
python app.py
```

## 📦 生产部署

### 使用 Gunicorn（Linux/macOS）
```bash
# 安装 Gunicorn
pip install gunicorn

# 运行应用
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用 uWSGI
```bash
# 安装 uWSGI
pip install uwsgi

# 创建 uwsgi.ini 配置文件
[uwsgi]
module = app:app
master = true
processes = 4
socket = /tmp/uwsgi.sock
chmod-socket = 666
vacuum = true
die-on-term = true
```

### 环境变量配置
生产环境需要设置：
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-strong-secret-key
DATABASE_URL=your-production-database-url
```

## 📞 技术支持

如果遇到问题：

1. 检查 Python 和 pip 版本
2. 确保虚拟环境已正确激活
3. 查看终端错误信息
4. 检查 `.env` 文件配置
5. 确保数据库文件存在且可访问
6. 查看 Flask 应用日志

## 🔧 开发工具推荐

### VS Code 推荐插件
- Python
- Python Docstring Generator
- autoDocstring
- GitLens
- Flask-Snippets

### PyCharm 配置
- 设置 Python 解释器为虚拟环境中的 Python
- 配置运行配置，设置环境变量
- 启用 Flask 支持

这样您就可以在任何电脑上快速配置和运行智能教学系统的后端环境了！ 