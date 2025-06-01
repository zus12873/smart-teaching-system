# 智能教学系统 Vue-App 环境配置指南

## 📋 系统要求

- **Node.js**: 16.0.0 或更高版本（推荐 18.x 或 20.x LTS）
- **npm**: 8.0.0 或更高版本（或 yarn/pnpm）
- **Git**: 用于克隆项目
- **操作系统**: Windows 10+、macOS 10.15+、Ubuntu 18.04+

## 🚀 快速开始

### 1. 安装 Node.js

#### Windows 系统
1. 访问 [Node.js官网](https://nodejs.org/)
2. 下载 LTS 版本（推荐 v18.x 或 v20.x）
3. 运行安装包，按照向导完成安装
4. 验证安装：
```bash
node --version
npm --version
```

#### macOS 系统
```bash
# 使用 Homebrew 安装（推荐）
brew install node

# 或者从官网下载安装包
# https://nodejs.org/
```

#### Linux (Ubuntu/Debian) 系统
```bash
# 更新包管理器
sudo apt update

# 安装 Node.js 和 npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

### 2. 克隆项目

```bash
# 克隆项目到本地
git clone <your-repository-url>
cd smart-teaching-system

# 或者如果已有项目文件，直接进入目录
cd smart-teaching-system
```

### 3. 配置 Vue 前端环境

```bash
# 进入 vue-app 目录
cd vue-app

# 安装依赖
npm install

# 如果 npm 安装速度慢，可以使用淘宝镜像
npm install --registry=https://registry.npm.taobao.org

# 或者使用 yarn（需要先安装 yarn）
# npm install -g yarn
# yarn install
```

### 4. 启动开发服务器

```bash
# 在 vue-app 目录下运行
npm run dev

# 或者
yarn dev
```

访问 http://localhost:5173 查看前端应用

## 🔧 详细配置说明

### 项目依赖说明

#### 核心依赖
- **Vue 3.5.13**: 前端框架
- **Vue Router 4.5.1**: 路由管理
- **Vite 6.3.5**: 构建工具和开发服务器

#### UI 和样式
- **Bootstrap 5.3.0**: UI 框架
- **Bootstrap Icons 1.13.1**: 图标库

#### 功能库
- **Axios 1.9.0**: HTTP 客户端
- **Chart.js 4.4.9**: 图表库
- **Markdown-it 14.1.0**: Markdown 解析器
- **Highlight.js 11.11.1**: 代码高亮

### 环境变量配置

在 `vue-app` 目录下创建 `.env` 文件：

```bash
# vue-app/.env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_APP_TITLE=智能教学系统
```

### 开发服务器配置

项目使用 Vite 作为开发服务器，配置在 `vite.config.js` 中：

- **端口**: 5173
- **API 代理**: `/api` 路径代理到 `http://127.0.0.1:5000`
- **CORS**: 已启用
- **热重载**: 自动启用

## 🛠️ 常用命令

```bash
# 开发环境运行
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview

# 安装新依赖
npm install <package-name>

# 安装开发依赖
npm install <package-name> --save-dev

# 更新依赖
npm update

# 清理 node_modules 并重新安装
rm -rf node_modules package-lock.json
npm install
```

## 🐛 常见问题解决

### 1. Node.js 版本问题
```bash
# 检查 Node.js 版本
node --version

# 如果版本过低，需要升级到 16+ 版本
# Windows: 从官网重新下载安装
# macOS: brew upgrade node
# Linux: 使用 nvm 管理 Node.js 版本
```

### 2. npm 安装依赖失败
```bash
# 清理 npm 缓存
npm cache clean --force

# 删除 node_modules 和 package-lock.json
rm -rf node_modules package-lock.json

# 重新安装
npm install

# 如果还是失败，尝试使用淘宝镜像
npm install --registry=https://registry.npm.taobao.org
```

### 3. 端口冲突
如果 5173 端口被占用：
```bash
# 方法1：杀死占用进程
# Windows: netstat -ano | findstr 5173
# macOS/Linux: lsof -ti:5173 | xargs kill

# 方法2：修改 vite.config.js 中的端口号
# server: { port: 3000 }

# 方法3：启动时指定端口
npm run dev -- --port 3000
```

### 4. 代理配置问题
确保后端 Flask 服务器在 http://127.0.0.1:5000 运行

### 5. 权限问题（Linux/macOS）
```bash
# 如果遇到权限问题
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) ./node_modules
```

## 🔄 项目更新

当项目有更新时：

```bash
# 拉取最新代码
git pull origin main

# 安装新依赖（如果 package.json 有变化）
npm install

# 重启开发服务器
npm run dev
```

## 📦 生产部署

### 构建项目
```bash
npm run build
```

构建完成后，`dist` 目录包含所有静态文件。

### 部署到 Web 服务器
将 `dist` 目录内容复制到 Web 服务器（如 Nginx、Apache）的根目录。

### Nginx 配置示例
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📞 技术支持

如果遇到问题：

1. 检查 Node.js 和 npm 版本
2. 查看终端错误信息
3. 检查 `package.json` 和 `vite.config.js` 配置
4. 确保后端服务正常运行
5. 查看浏览器开发者工具的控制台

## 🔧 IDE 推荐配置

### VS Code 推荐插件
- Vue Language Features (Volar)
- TypeScript Vue Plugin (Volar)
- Auto Rename Tag
- Bracket Pair Colorizer
- GitLens
- Prettier
- ESLint

### VS Code 配置文件
在项目根目录创建 `.vscode/settings.json`：
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "files.associations": {
    "*.vue": "vue"
  }
}
```

这样您就可以在任何电脑上快速配置和运行智能教学系统的前端环境了！ 