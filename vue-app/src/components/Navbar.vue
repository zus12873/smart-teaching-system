<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <!-- Logo和系统名称 -->
      <router-link class="navbar-brand" to="/">
        <i class="bi bi-mortarboard-fill me-2"></i>
        智能教学系统
      </router-link>

      <!-- 移动端菜单按钮 -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <!-- 主导航菜单 -->
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">
              <i class="bi bi-house me-1"></i>首页
            </router-link>
          </li>
          
          <!-- 根据用户角色显示不同菜单 -->
          <template v-if="isAuthenticated">
            <!-- 管理员菜单 -->
            <template v-if="isAdmin">
              <li class="nav-item dropdown">
                <a
                  class="nav-link dropdown-toggle"
                  href="#"
                  role="button"
                  data-bs-toggle="dropdown"
                >
                  <i class="bi bi-gear me-1"></i>管理
                </a>
                <ul class="dropdown-menu">
                  <li>
                    <router-link class="dropdown-item" to="/admin/dashboard">
                      <i class="bi bi-speedometer2 me-2"></i>仪表板
                    </router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/admin/users">
                      <i class="bi bi-people me-2"></i>用户管理
                    </router-link>
                  </li>
                  <li>
                    <router-link class="dropdown-item" to="/admin/courses">
                      <i class="bi bi-book me-2"></i>课程管理
                    </router-link>
                  </li>
                </ul>
              </li>
            </template>

            <!-- 教师菜单 -->
            <template v-if="isTeacher">
              <li class="nav-item">
                <router-link class="nav-link" to="/teacher/dashboard">
                  <i class="bi bi-person-badge me-1"></i>教师面板
                </router-link>
              </li>
            </template>

            <!-- 学生菜单 -->
            <template v-if="isStudent">
              <li class="nav-item">
                <router-link class="nav-link" to="/student/dashboard">
                  <i class="bi bi-mortarboard me-1"></i>学生面板
                </router-link>
              </li>
            </template>

            <!-- 智能功能菜单（所有角色都可访问） -->
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
              >
                <i class="bi bi-magic me-1"></i>智能功能
              </a>
              <ul class="dropdown-menu">
                <li>
                  <router-link class="dropdown-item" to="/problem-generation">
                    <i class="bi bi-lightbulb me-2"></i>智能出题
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" to="/multi-upload">
                    <i class="bi bi-files me-2"></i>智能批改
                  </router-link>
                </li>
              </ul>
            </li>
          </template>
        </ul>

        <!-- 用户信息和操作 -->
        <ul class="navbar-nav">
          <template v-if="isAuthenticated">
            <!-- 用户信息下拉菜单 -->
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle user-menu"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
              >
                <div class="user-avatar">
                  <i class="bi bi-person-circle"></i>
                </div>
                <div class="user-info">
                  <span class="username">{{ user.username }}</span>
                  <span class="user-role" :class="roleClass">{{ roleText }}</span>
                </div>
              </a>
              <ul class="dropdown-menu dropdown-menu-end">
                <li>
                  <h6 class="dropdown-header">
                    <i class="bi bi-person me-2"></i>{{ user.username }}
                  </h6>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item" href="#" @click="handleProfile">
                    <i class="bi bi-person-gear me-2"></i>个人设置
                  </a>
                </li>
                <li>
                  <a class="dropdown-item" href="#" @click="handleHelp">
                    <i class="bi bi-question-circle me-2"></i>帮助中心
                  </a>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item text-danger" href="#" @click="handleLogout">
                    <i class="bi bi-box-arrow-right me-2"></i>退出登录
                  </a>
                </li>
              </ul>
            </li>
          </template>
          
          <!-- 未登录时显示登录按钮 -->
          <template v-else>
            <li class="nav-item">
              <router-link class="nav-link" to="/login">
                <i class="bi bi-box-arrow-in-right me-1"></i>登录
              </router-link>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { user, isAuthenticated, isAdmin, isTeacher, isStudent, logout } from '../stores/auth'

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter()

    // 角色相关的计算属性
    const roleText = computed(() => {
      if (!user.value) return ''
      switch (user.value.role) {
        case 'admin': return '管理员'
        case 'teacher': return '教师'
        case 'student': return '学生'
        default: return '用户'
      }
    })

    const roleClass = computed(() => {
      if (!user.value) return ''
      switch (user.value.role) {
        case 'admin': return 'role-admin'
        case 'teacher': return 'role-teacher'
        case 'student': return 'role-student'
        default: return ''
      }
    })

    // 处理登出
    const handleLogout = async () => {
      try {
        await logout()
        await router.push('/login')
      } catch (error) {
        console.error('登出失败:', error)
      }
    }

    // 处理个人设置
    const handleProfile = () => {
      router.push('/profile')
    }

    // 处理帮助中心
    const handleHelp = () => {
      // TODO: 实现帮助中心页面
      alert('帮助中心功能开发中...')
    }

    return {
      user,
      isAuthenticated,
      isAdmin,
      isTeacher,
      isStudent,
      roleText,
      roleClass,
      handleLogout,
      handleProfile,
      handleHelp
    }
  }
}
</script>

<style scoped>
.navbar {
  box-shadow: 0 2px 4px rgba(33, 150, 243, 0.1); /* 蓝色阴影 */
}

.navbar-brand {
  font-weight: 600;
  font-size: 1.25rem;
}

.user-menu {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem !important;
}

.user-avatar {
  font-size: 1.5rem;
  margin-right: 0.5rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.2;
}

.username {
  font-weight: 500;
  font-size: 0.9rem;
}

.user-role {
  font-size: 0.75rem;
  opacity: 0.8;
  padding: 1px 6px;
  border-radius: 10px;
  margin-top: 2px;
}

.role-admin {
  background-color: rgba(220, 53, 69, 0.2);
  color: #dc3545;
}

.role-teacher {
  background-color: rgba(25, 135, 84, 0.2);
  color: #198754;
}

.role-student {
  background-color: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.dropdown-header {
  color: #495057;
  font-weight: 600;
}

.dropdown-item {
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.dropdown-item.text-danger:hover {
  background-color: #f8d7da;
  color: #721c24 !important;
}

.nav-link {
  transition: all 0.2s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.router-link-active {
  background-color: rgba(255, 255, 255, 0.2) !important;
  border-radius: 4px;
}

@media (max-width: 991px) {
  .user-menu {
    flex-direction: row;
    justify-content: flex-start;
  }
  
  .user-info {
    margin-left: 0.5rem;
  }
  
  .dropdown-menu {
    position: static !important;
    transform: none !important;
    border: none;
    box-shadow: none;
    background-color: rgba(255, 255, 255, 0.1);
    margin-top: 0.5rem;
  }
  
  .dropdown-item {
    color: rgba(255, 255, 255, 0.8);
  }
  
  .dropdown-item:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
  }
}
</style> 