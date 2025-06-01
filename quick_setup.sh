#!/bin/bash

# 智能教学系统快速环境配置脚本
# 适用于 Linux/macOS 系统

set -e

echo "🚀 智能教学系统环境配置开始..."
echo "=================================="

# 检查系统类型
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SYSTEM="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    SYSTEM="macOS"
else
    echo "❌ 不支持的操作系统类型: $OSTYPE"
    exit 1
fi

echo "📍 检测到系统: $SYSTEM"

# 检查 Python 是否安装
echo "🔍 检查 Python 环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✅ Python 已安装: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    echo "✅ Python 已安装: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    echo "❌ Python 未安装，请先安装 Python 3.8+"
    exit 1
fi

# 检查 Node.js 是否安装
echo "🔍 检查 Node.js 环境..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js 已安装: $NODE_VERSION"
else
    echo "❌ Node.js 未安装，请先安装 Node.js 16+"
    exit 1
fi

# 检查 npm 是否安装
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✅ npm 已安装: $NPM_VERSION"
else
    echo "❌ npm 未安装，请先安装 npm"
    exit 1
fi

echo ""
echo "🐍 配置 Python 后端环境..."
echo "=================================="

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    $PYTHON_CMD -m venv venv
    echo "✅ 虚拟环境创建完成"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo "⬆️ 升级 pip..."
pip install --upgrade pip

# 安装 Python 依赖
if [ -f "requirements.txt" ]; then
    echo "📦 安装 Python 依赖..."
    pip install -r requirements.txt
    echo "✅ Python 依赖安装完成"
else
    echo "⚠️ requirements.txt 不存在，手动安装核心依赖..."
    pip install flask flask-sqlalchemy flask-login flask-cors python-dotenv requests
    echo "✅ 核心依赖安装完成"
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "📝 创建 .env 文件..."
    cat > .env << EOF
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-$(date +%s)
DATABASE_URL=sqlite:///instance/database.db
DIFY_API_KEY=your-dify-api-key
DIFY_API_URL=https://api.dify.ai/v1
EOF
    echo "✅ .env 文件创建完成，请根据需要修改配置"
else
    echo "✅ .env 文件已存在"
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p instance uploads uploads/txt templates
echo "✅ 目录创建完成"

echo ""
echo "🌐 配置 Vue.js 前端环境..."
echo "=================================="

# 进入 vue-app 目录
if [ -d "vue-app" ]; then
    cd vue-app
    
    # 安装 Node.js 依赖
    if [ -f "package.json" ]; then
        echo "📦 安装 Vue.js 依赖..."
        npm install
        echo "✅ Vue.js 依赖安装完成"
    else
        echo "❌ vue-app/package.json 不存在"
        exit 1
    fi
    
    # 检查前端 .env 文件
    if [ ! -f ".env" ]; then
        echo "📝 创建前端 .env 文件..."
        cat > .env << EOF
VITE_API_BASE_URL=http://localhost:5000/api
VITE_APP_TITLE=智能教学系统
EOF
        echo "✅ 前端 .env 文件创建完成"
    else
        echo "✅ 前端 .env 文件已存在"
    fi
    
    cd ..
else
    echo "⚠️ vue-app 目录不存在，跳过前端配置"
fi

echo ""
echo "🎉 环境配置完成！"
echo "=================================="
echo ""
echo "📋 下一步操作："
echo "1. 启动后端服务器:"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "2. 启动前端开发服务器 (新终端):"
echo "   cd vue-app"
echo "   npm run dev"
echo ""
echo "3. 访问应用:"
echo "   前端: http://localhost:5173"
echo "   后端: http://localhost:5000"
echo ""
echo "📖 详细文档请查看:"
echo "   - SETUP_GUIDE.md (Vue.js 前端)"
echo "   - FLASK_SETUP_GUIDE.md (Flask 后端)"
echo ""
echo "🚀 配置完成，祝您使用愉快！" 