@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 智能教学系统快速环境配置脚本
:: 适用于 Windows 系统

echo 🚀 智能教学系统环境配置开始...
echo ==================================

:: 检查 Python 是否安装
echo 🔍 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python 已安装: !PYTHON_VERSION!
    set PYTHON_CMD=python
) else (
    echo ❌ Python 未安装，请先安装 Python 3.8+
    echo 📥 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查 Node.js 是否安装
echo 🔍 检查 Node.js 环境...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    echo ✅ Node.js 已安装: !NODE_VERSION!
) else (
    echo ❌ Node.js 未安装，请先安装 Node.js 16+
    echo 📥 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

:: 检查 npm 是否安装
echo 🔍 检查 npm 环境...
npm --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=1" %%i in ('npm --version 2^>^&1') do set NPM_VERSION=%%i
    echo ✅ npm 已安装: !NPM_VERSION!
) else (
    echo ❌ npm 未安装，请重新安装 Node.js
    pause
    exit /b 1
)

echo.
echo 🐍 配置 Python 后端环境...
echo ==================================

:: 创建虚拟环境
if not exist "venv" (
    echo 📦 创建虚拟环境...
    %PYTHON_CMD% -m venv venv
    echo ✅ 虚拟环境创建完成
) else (
    echo ✅ 虚拟环境已存在
)

:: 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

:: 升级 pip
echo ⬆️ 升级 pip...
python -m pip install --upgrade pip

:: 安装 Python 依赖
if exist "requirements.txt" (
    echo 📦 安装 Python 依赖...
    pip install -r requirements.txt
    echo ✅ Python 依赖安装完成
) else (
    echo ⚠️ requirements.txt 不存在，手动安装核心依赖...
    pip install flask flask-sqlalchemy flask-login flask-cors python-dotenv requests
    echo ✅ 核心依赖安装完成
)

:: 检查 .env 文件
if not exist ".env" (
    echo 📝 创建 .env 文件...
    (
        echo FLASK_APP=app.py
        echo FLASK_ENV=development
        echo FLASK_DEBUG=True
        echo SECRET_KEY=your-secret-key-%RANDOM%
        echo DATABASE_URL=sqlite:///instance/database.db
        echo DIFY_API_KEY=your-dify-api-key
        echo DIFY_API_URL=https://api.dify.ai/v1
    ) > .env
    echo ✅ .env 文件创建完成，请根据需要修改配置
) else (
    echo ✅ .env 文件已存在
)

:: 创建必要的目录
echo 📁 创建必要的目录...
if not exist "instance" mkdir instance
if not exist "uploads" mkdir uploads
if not exist "uploads\txt" mkdir uploads\txt
if not exist "templates" mkdir templates
echo ✅ 目录创建完成

echo.
echo 🌐 配置 Vue.js 前端环境...
echo ==================================

:: 检查 vue-app 目录
if exist "vue-app" (
    cd vue-app
    
    :: 检查 package.json 文件
    if exist "package.json" (
        echo 📦 安装 Vue.js 依赖...
        npm install
        echo ✅ Vue.js 依赖安装完成
    ) else (
        echo ❌ vue-app\package.json 不存在
        pause
        exit /b 1
    )
    
    :: 检查前端 .env 文件
    if not exist ".env" (
        echo 📝 创建前端 .env 文件...
        (
            echo VITE_API_BASE_URL=http://localhost:5000/api
            echo VITE_APP_TITLE=智能教学系统
        ) > .env
        echo ✅ 前端 .env 文件创建完成
    ) else (
        echo ✅ 前端 .env 文件已存在
    )
    
    cd ..
) else (
    echo ⚠️ vue-app 目录不存在，跳过前端配置
)

echo.
echo 🎉 环境配置完成！
echo ==================================
echo.
echo 📋 下一步操作：
echo 1. 启动后端服务器:
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 2. 启动前端开发服务器 (新命令提示符):
echo    cd vue-app
echo    npm run dev
echo.
echo 3. 访问应用:
echo    前端: http://localhost:5173
echo    后端: http://localhost:5000
echo.
echo 📖 详细文档请查看:
echo    - SETUP_GUIDE.md (Vue.js 前端)
echo    - FLASK_SETUP_GUIDE.md (Flask 后端)
echo.
echo 🚀 配置完成，祝您使用愉快！
echo.
pause 