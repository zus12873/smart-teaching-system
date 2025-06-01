<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <i class="bi bi-mortarboard-fill"></i>
        </div>
        <h2>智能教学系统</h2>
        <p class="text-muted">请登录您的账户</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="mb-3">
          <label for="username" class="form-label">
            <i class="bi bi-person me-2"></i>用户名
          </label>
          <input
            type="text"
            class="form-control"
            id="username"
            v-model="loginForm.username"
            :class="{ 'is-invalid': errors.username }"
            placeholder="请输入用户名"
            required
            autocomplete="username"
          >
          <div v-if="errors.username" class="invalid-feedback">
            {{ errors.username }}
          </div>
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">
            <i class="bi bi-lock me-2"></i>密码
          </label>
          <div class="input-group">
            <input
              :type="showPassword ? 'text' : 'password'"
              class="form-control"
              id="password"
              v-model="loginForm.password"
              :class="{ 'is-invalid': errors.password }"
              placeholder="请输入密码"
              required
              autocomplete="current-password"
            >
            <button
              type="button"
              class="btn btn-outline-secondary"
              @click="togglePassword"
            >
              <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </button>
          </div>
          <div v-if="errors.password" class="invalid-feedback d-block">
            {{ errors.password }}
          </div>
        </div>

        <div class="mb-3 form-check">
          <input
            type="checkbox"
            class="form-check-input"
            id="rememberMe"
            v-model="loginForm.rememberMe"
          >
          <label class="form-check-label" for="rememberMe">
            记住我
          </label>
        </div>

        <div v-if="errorMessage" class="alert alert-danger" role="alert">
          <i class="bi bi-exclamation-triangle me-2"></i>
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          class="btn btn-primary w-100"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
          <i v-else class="bi bi-box-arrow-in-right me-2"></i>
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
      </form>

      <div class="login-footer">
        <div class="demo-accounts">
          <h6>演示账号</h6>
          <div class="demo-account-list">
            <button
              type="button"
              class="btn btn-outline-info btn-sm"
              @click="fillDemoAccount('admin')"
            >
              <i class="bi bi-shield-check me-1"></i>管理员
            </button>
            <button
              type="button"
              class="btn btn-outline-success btn-sm"
              @click="fillDemoAccount('teacher')"
            >
              <i class="bi bi-person-badge me-1"></i>教师
            </button>
            <button
              type="button"
              class="btn btn-outline-warning btn-sm"
              @click="fillDemoAccount('student')"
            >
              <i class="bi bi-mortarboard me-1"></i>学生
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="system-info">
      <p class="text-muted small">
        <i class="bi bi-info-circle me-1"></i>
        智能教学系统 v1.0 | 基于AI的智能出题与批改平台
      </p>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { login, isLoading, getDefaultRoute } from '../stores/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const showPassword = ref(false)
    const errorMessage = ref('')

    const loginForm = reactive({
      username: '',
      password: '',
      rememberMe: false
    })

    const errors = reactive({
      username: '',
      password: ''
    })

    // 演示账号数据
    const demoAccounts = {
      admin: { username: 'admin', password: 'admin' },
      teacher: { username: 'teacher', password: 'teacher' },
      student: { username: 'student', password: 'student' }
    }

    const validateForm = () => {
      errors.username = ''
      errors.password = ''
      
      if (!loginForm.username.trim()) {
        errors.username = '请输入用户名'
        return false
      }
      
      if (!loginForm.password.trim()) {
        errors.password = '请输入密码'
        return false
      }
      
      if (loginForm.password.length < 3) {
        errors.password = '密码长度至少3位'
        return false
      }
      
      return true
    }

    const handleLogin = async () => {
      errorMessage.value = ''
      
      if (!validateForm()) {
        return
      }

      try {
        console.log('尝试登录:', loginForm.username)
        const result = await login({
          username: loginForm.username,
          password: loginForm.password
        })

        if (result.success) {
          console.log('登录成功:', result.user)
          // 登录成功，稍微延迟后根据用户角色跳转，确保会话完全建立
          setTimeout(async () => {
            const defaultRoute = getDefaultRoute(result.user.role)
            await router.push(defaultRoute)
          }, 100) // 100毫秒延迟
        } else {
          console.log('登录失败:', result.message)
          errorMessage.value = result.message || '登录失败'
        }
      } catch (error) {
        console.error('登录错误:', error)
        errorMessage.value = '登录失败，请稍后重试'
      }
    }

    const togglePassword = () => {
      showPassword.value = !showPassword.value
    }

    const fillDemoAccount = (role) => {
      const account = demoAccounts[role]
      if (account) {
        loginForm.username = account.username
        loginForm.password = account.password
        errorMessage.value = ''
        errors.username = ''
        errors.password = ''
      }
    }

    // 检查URL参数中是否有重定向地址
    onMounted(() => {
      const urlParams = new URLSearchParams(window.location.search)
      const redirect = urlParams.get('redirect')
      if (redirect) {
        console.log('登录后将重定向到:', redirect)
      }
    })

    return {
      loginForm,
      errors,
      errorMessage,
      showPassword,
      isLoading,
      handleLogin,
      togglePassword,
      fillDemoAccount
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); /* 浅蓝色渐变 */
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(33, 150, 243, 0.15); /* 蓝色阴影 */
  padding: 40px;
  width: 100%;
  max-width: 400px;
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  font-size: 3rem;
  color: #1976d2; /* 调整为蓝色 */
  margin-bottom: 15px;
}

.login-header h2 {
  color: #1565c0; /* 调整为深蓝色 */
  font-weight: 600;
  margin-bottom: 8px;
}

.login-form .form-label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 8px;
}

.form-control {
  border-radius: 8px;
  border: 1px solid #e1e5e9;
  padding: 12px 16px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #1976d2; /* 蓝色聚焦边框 */
  box-shadow: 0 0 0 0.2rem rgba(25, 118, 210, 0.25); /* 蓝色聚焦阴影 */
}

.btn-primary {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); /* 蓝色渐变按钮 */
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(25, 118, 210, 0.3); /* 蓝色悬停阴影 */
}

.btn-primary:disabled {
  transform: none;
  box-shadow: none;
}

.login-footer {
  margin-top: 30px;
  text-align: center;
}

.demo-accounts h6 {
  color: #6c757d;
  margin-bottom: 15px;
  font-size: 14px;
}

.demo-account-list {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

.demo-account-list .btn {
  border-radius: 20px;
  font-size: 12px;
  padding: 6px 12px;
}

.system-info {
  margin-top: 30px;
  text-align: center;
}

.system-info p {
  color: rgba(25, 118, 210, 0.8); /* 调整为蓝色透明文字 */
  margin: 0;
}

.alert {
  border-radius: 8px;
  border: none;
  font-size: 14px;
}

.form-check-label {
  font-size: 14px;
  color: #6c757d;
}

.input-group .btn {
  border-left: none;
}

.input-group .form-control:focus + .btn {
  border-color: #1976d2; /* 蓝色边框 */
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
    margin: 10px;
  }
  
  .demo-account-list {
    flex-direction: column;
    align-items: center;
  }
  
  .demo-account-list .btn {
    width: 120px;
  }
}
</style> 