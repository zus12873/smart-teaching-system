import { ref, computed } from 'vue'
import { authAPI } from '../utils/api'

// 用户状态
const user = ref(null)
const isLoading = ref(false)

// 计算属性
const isAuthenticated = computed(() => !!user.value)
const userRole = computed(() => user.value?.role || null)
const isAdmin = computed(() => user.value?.role === 'admin')
const isTeacher = computed(() => user.value?.role === 'teacher')
const isStudent = computed(() => user.value?.role === 'student')

// 登录函数
const login = async (credentials) => {
  isLoading.value = true
  try {
    const response = await authAPI.login(credentials)
    if (response.data.success) {
      user.value = response.data.user
      // 保存到localStorage
      localStorage.setItem('user', JSON.stringify(response.data.user))
      
      // 验证会话是否正确建立（稍微延迟后验证）
      setTimeout(async () => {
        try {
          await getCurrentUser()
        } catch (error) {
          console.warn('会话验证失败，但登录成功')
        }
      }, 50)
      
      return { success: true, user: response.data.user }
    } else {
      return { success: false, message: response.data.message }
    }
  } catch (error) {
    console.error('登录失败:', error)
    return { 
      success: false, 
      message: error.response?.data?.message || '登录失败，请稍后重试' 
    }
  } finally {
    isLoading.value = false
  }
}

// 登出函数
const logout = async () => {
  try {
    await authAPI.logout()
  } catch (error) {
    console.error('登出请求失败:', error)
  } finally {
    // 无论API调用是否成功，都清除本地状态
    user.value = null
    localStorage.removeItem('user')
  }
}

// 获取当前用户信息
const getCurrentUser = async (retryCount = 0) => {
  try {
    const response = await authAPI.getCurrentUser()
    if (response.data.success) {
      user.value = response.data.user
      localStorage.setItem('user', JSON.stringify(response.data.user))
      return response.data.user
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    
    // 如果是401错误且还没重试过，则稍后重试一次
    if (error.response?.status === 401 && retryCount < 1) {
      console.log('会话可能还在建立中，稍后重试...')
      await new Promise(resolve => setTimeout(resolve, 1000))
      return getCurrentUser(retryCount + 1)
    }
    
    // 清除无效的本地存储
    user.value = null
    localStorage.removeItem('user')
  }
  return null
}

// 初始化用户状态（从localStorage恢复）
const initializeAuth = async () => {
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    try {
      user.value = JSON.parse(savedUser)
      // 验证用户状态是否仍然有效
      await getCurrentUser()
    } catch (error) {
      console.error('初始化用户状态失败:', error)
      localStorage.removeItem('user')
    }
  }
}

// 根据用户角色获取默认路由
const getDefaultRoute = (userRole) => {
  switch (userRole) {
    case 'admin':
      return '/admin/dashboard'
    case 'teacher':
      return '/teacher/dashboard'
    case 'student':
      return '/student/dashboard'
    default:
      return '/'
  }
}

export {
  // 状态
  user,
  isLoading,
  
  // 计算属性
  isAuthenticated,
  userRole,
  isAdmin,
  isTeacher,
  isStudent,
  
  // 方法
  login,
  logout,
  getCurrentUser,
  initializeAuth,
  getDefaultRoute
} 