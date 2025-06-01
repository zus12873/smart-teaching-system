#!/bin/bash

# 智能教学系统开发环境启动脚本

echo "🚀 启动智能教学系统开发环境..."

# 检查是否安装了必要的依赖
echo "📦 检查依赖..."

# 检查Python依赖
if ! python -c "import flask_cors" 2>/dev/null; then
    echo "⚠️  缺少 flask-cors 依赖，正在安装..."
    pip install flask-cors
fi

# 启动API后端服务器
echo "🔧 启动API后端服务器 (端口 5000)..."
python api_app.py &
API_PID=$!

# 等待API服务器启动
sleep 3

# 启动Vue前端开发服务器
echo "🎨 启动Vue前端开发服务器 (端口 5174)..."
cd vue-app
npm run dev &
VUE_PID=$!

# 等待Vue服务器启动
sleep 5

echo "✅ 开发环境启动完成！"
echo ""
echo "📍 访问地址："
echo "   前端应用: http://localhost:5174"
echo "   API后端:  http://localhost:5000/api"
echo ""
echo "🔑 默认管理员账号："
echo "   用户名: admin"
echo "   密码:   admin"
echo ""
echo "⚡ 功能页面："
echo "   智能出题: http://localhost:5174/problem-generation"
echo "   智能批改: http://localhost:5174/multi-upload"
echo "   管理面板: http://localhost:5174/admin/dashboard"
echo ""
echo "🛑 按 Ctrl+C 停止所有服务"

# 等待用户中断
wait

# 清理进程
echo "🧹 正在停止服务..."
kill $API_PID 2>/dev/null
kill $VUE_PID 2>/dev/null
echo "✅ 所有服务已停止" 