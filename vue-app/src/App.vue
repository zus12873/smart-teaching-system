<script>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { initializeAuth } from './stores/auth'

export default {
  name: 'App',
  components: {
    Navbar
  },
  setup() {
    const route = useRoute()
    const isLoginPage = computed(() => route.path === '/login')

    onMounted(async () => {
      await initializeAuth()
    })

    return {
      isLoginPage
    }
  }
}
</script>

<template>
  <div id="app">
    <!-- 固定在顶端的导航栏 -->
    <header class="site-header" v-if="!isLoginPage">
      <Navbar />
    </header>

    <!-- 主要内容区域 -->
    <div class="main-container" :class="{ 'login-layout': isLoginPage }">
      <router-view />
    </div>

    <!-- 固定在底部的页脚 -->
    <footer class="site-footer" v-if="!isLoginPage">
      <div class="container text-center py-3">
        <span class="text-muted">© 2024 智能教学系统. All rights reserved.</span>
      </div>
    </footer>
  </div>
</template>

<style>
/* 全局 & 布局 */
body {
  margin: 0;
  padding: 0;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background-color: #e3f2fd; /* 浅蓝色背景 */
  color: #333;
}
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #e3f2fd; /* 浅蓝色背景 */
}

/* 固定在顶部的导航栏 */
.site-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background: #fff;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.15); /* 调整阴影颜色 */
}

/* 主容器样式：上下都留空间 */
.main-container {
  margin: 80px auto 80px; /* 上 80px（header 高度+空隙），下 80px（footer 高度+空隙） */
  max-width: 1200px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(33, 150, 243, 0.15); /* 调整阴影颜色 */
  padding: 30px;
  flex: 1;
}

/* 登录页不需要卡片式布局 */
.main-container.login-layout {
  margin: 0;
  max-width: none;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
  padding: 0;
}

/* 页面头部样式 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
  border-bottom: 2px solid #1976d2; /* 调整为蓝色 */
  padding-bottom: 20px;
}
.page-header h1 {
  color: #1565c0; /* 调整为深蓝色 */
  font-weight: 600;
}
.page-header p {
  color: #424242; /* 调整文字颜色 */
  font-size: 16px;
}

/* 按钮样式 */
.btn-primary {
  background-color: #1976d2; /* 蓝色按钮 */
  border-color: #1976d2;
}
.btn-primary:hover {
  background-color: #1565c0; /* 深蓝色悬停 */
  border-color: #1565c0;
}

/* 卡片样式 */
.card {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(33, 150, 243, 0.1); /* 蓝色阴影 */
  margin-bottom: 20px;
  transition: all 0.3s;
}
.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(33, 150, 243, 0.2); /* 加强蓝色阴影 */
}
.card-header {
  background-color: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
  font-weight: 600;
}

/* 表单样式 */
.form-control {
  border-radius: 6px;
  border: 1px solid #ced4da;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}
.form-control:focus {
  border-color: #1976d2; /* 蓝色聚焦边框 */
  box-shadow: 0 0 0 0.2rem rgba(25, 118, 210, 0.25); /* 蓝色聚焦阴影 */
}

/* 表格样式 */
.table {
  border-radius: 8px;
  overflow: hidden;
}
.table thead th {
  background-color: #1976d2; /* 蓝色表头 */
  color: white;
  border: none;
  font-weight: 600;
}

/* 警告框样式 */
.alert {
  border-radius: 8px;
  border: none;
}
.alert-info {
  background-color: #e7f3ff;
  color: #0c5460;
}
.alert-success {
  background-color: #d1edcc;
  color: #0a3622;
}
.alert-warning {
  background-color: #fff3cd;
  color: #856404;
}
.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-container {
    margin: 80px 15px 80px;
    padding: 20px;
  }
  .page-header h1 {
    font-size: 1.5rem;
  }
}
@media (max-width: 576px) {
  .main-container {
    margin: 80px 10px 80px;
    padding: 15px;
  }
  .page-header {
    margin-bottom: 20px;
    padding-bottom: 15px;
  }
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 加载动画 */
.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 工具提示样式 */
.tooltip {
  font-size: 0.875rem;
}

/* 徽章样式 */
.badge {
  font-size: 0.75em;
}

/* 分页样式 */
.pagination {
  justify-content: center;
}
.page-link {
  color: #1976d2; /* 蓝色分页链接 */
  border-color: #dee2e6;
}
.page-link:hover {
  color: #1565c0; /* 深蓝色悬停 */
  background-color: #e3f2fd; /* 浅蓝色背景 */
  border-color: #dee2e6;
}
.page-item.active .page-link {
  background-color: #1976d2; /* 蓝色激活状态 */
  border-color: #1976d2;
}

/* 固定在底部的页脚 */
.site-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: #fff;
  box-shadow: 0 -2px 8px rgba(33, 150, 243, 0.15); /* 蓝色阴影 */
  z-index: 1000;
}
</style>