<template>
  <div class="user-profile">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-person-circle me-2"></i>个人信息
        </h5>
      </div>
      
      <div class="card-body">
        <form @submit.prevent="updateProfile" v-if="!isLoading">
          <div class="row">
            <div class="col-md-6">
              <div class="mb-3">
                <label for="username" class="form-label">用户名</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="profileForm.username"
                  :class="{ 'is-invalid': errors.username }"
                  required
                >
                <div v-if="errors.username" class="invalid-feedback">
                  {{ errors.username }}
                </div>
              </div>
            </div>
            
            <div class="col-md-6">
              <div class="mb-3">
                <label for="email" class="form-label">邮箱地址</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="profileForm.email"
                  :class="{ 'is-invalid': errors.email }"
                  required
                >
                <div v-if="errors.email" class="invalid-feedback">
                  {{ errors.email }}
                </div>
              </div>
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6">
              <div class="mb-3">
                <label for="role" class="form-label">角色</label>
                <input
                  type="text"
                  class="form-control"
                  id="role"
                  :value="getRoleText(profileForm.role)"
                  readonly
                >
              </div>
            </div>
            
            <div class="col-md-6">
              <div class="mb-3">
                <label for="newPassword" class="form-label">新密码（可选）</label>
                <input
                  type="password"
                  class="form-control"
                  id="newPassword"
                  v-model="profileForm.newPassword"
                  :class="{ 'is-invalid': errors.newPassword }"
                  placeholder="留空表示不修改密码"
                >
                <div v-if="errors.newPassword" class="invalid-feedback">
                  {{ errors.newPassword }}
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="message" class="alert" :class="messageType === 'success' ? 'alert-success' : 'alert-danger'">
            {{ message }}
          </div>
          
          <div class="d-flex justify-content-end">
            <button type="button" class="btn btn-secondary me-2" @click="resetForm">
              重置
            </button>
            <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
              保存修改
            </button>
          </div>
        </form>
        
        <div v-else class="text-center">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">加载中...</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { user } from '../stores/auth'
import { authAPI } from '../utils/api'

export default {
  name: 'UserProfile',
  setup() {
    const isLoading = ref(true)
    const isSubmitting = ref(false)
    const message = ref('')
    const messageType = ref('success')
    
    const profileForm = reactive({
      username: '',
      email: '',
      role: '',
      newPassword: ''
    })
    
    const errors = reactive({
      username: '',
      email: '',
      newPassword: ''
    })
    
    const loadUserProfile = () => {
      if (user.value) {
        profileForm.username = user.value.username
        profileForm.email = user.value.email
        profileForm.role = user.value.role
        profileForm.newPassword = ''
        isLoading.value = false
      }
    }
    
    const getRoleText = (role) => {
      const roleMap = {
        'admin': '管理员',
        'teacher': '教师',
        'student': '学生'
      }
      return roleMap[role] || role
    }
    
    const validateForm = () => {
      errors.username = ''
      errors.email = ''
      errors.newPassword = ''
      
      if (!profileForm.username.trim()) {
        errors.username = '用户名不能为空'
        return false
      }
      
      if (!profileForm.email.trim()) {
        errors.email = '邮箱不能为空'
        return false
      }
      
      if (profileForm.newPassword && profileForm.newPassword.length < 6) {
        errors.newPassword = '密码长度至少6位'
        return false
      }
      
      return true
    }
    
    const updateProfile = async () => {
      if (!validateForm()) return
      
      isSubmitting.value = true
      message.value = ''
      
      try {
        // 构建更新数据
        const updateData = {
          username: profileForm.username,
          email: profileForm.email
        }
        
        if (profileForm.newPassword) {
          updateData.password = profileForm.newPassword
        }
        
        // 这里需要后端提供用户自己更新信息的API
        // const response = await authAPI.updateProfile(updateData)
        
        // 模拟API调用成功
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        message.value = '个人信息更新成功'
        messageType.value = 'success'
        
        // 清空密码字段
        profileForm.newPassword = ''
        
        // 更新本地用户信息
        user.value = { ...user.value, username: profileForm.username, email: profileForm.email }
        localStorage.setItem('user', JSON.stringify(user.value))
        
      } catch (error) {
        console.error('更新个人信息失败:', error)
        message.value = error.response?.data?.message || '更新失败，请稍后重试'
        messageType.value = 'error'
      } finally {
        isSubmitting.value = false
      }
    }
    
    const resetForm = () => {
      loadUserProfile()
      message.value = ''
      Object.keys(errors).forEach(key => errors[key] = '')
    }
    
    onMounted(() => {
      loadUserProfile()
    })
    
    return {
      isLoading,
      isSubmitting,
      message,
      messageType,
      profileForm,
      errors,
      getRoleText,
      updateProfile,
      resetForm
    }
  }
}
</script>

<style scoped>
.user-profile {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.form-label {
  font-weight: 500;
  color: #495057;
}

.alert {
  border-radius: 6px;
  border: none;
}
</style> 