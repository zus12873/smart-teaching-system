<template>
  <div class="api-test">
    <div class="container mt-4">
      <h2>API连接测试</h2>
      
      <div class="row">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5>健康检查</h5>
            </div>
            <div class="card-body">
              <button @click="testHealth" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                测试健康检查
              </button>
              <div v-if="healthResult" class="mt-3">
                <div class="alert" :class="healthResult.success ? 'alert-success' : 'alert-danger'">
                  <strong>结果:</strong> {{ healthResult.message }}
                  <br>
                  <small>时间: {{ healthResult.timestamp }}</small>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5>登录测试</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label">用户名</label>
                <input v-model="testCredentials.username" class="form-control" placeholder="admin">
              </div>
              <div class="mb-3">
                <label class="form-label">密码</label>
                <input v-model="testCredentials.password" type="password" class="form-control" placeholder="admin">
              </div>
              <button @click="testLogin" class="btn btn-success" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                测试登录
              </button>
              <div v-if="loginResult" class="mt-3">
                <div class="alert" :class="loginResult.success ? 'alert-success' : 'alert-danger'">
                  <strong>结果:</strong> {{ loginResult.message }}
                  <div v-if="loginResult.user" class="mt-2">
                    <small>
                      用户: {{ loginResult.user.username }} ({{ loginResult.user.role }})
                    </small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row mt-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h5>网络信息</h5>
            </div>
            <div class="card-body">
              <p><strong>前端地址:</strong> {{ frontendUrl }}</p>
              <p><strong>API地址:</strong> {{ apiUrl }}</p>
              <p><strong>浏览器:</strong> {{ userAgent }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import api, { authAPI } from '../utils/api'

export default {
  name: 'ApiTest',
  setup() {
    const loading = ref(false)
    const healthResult = ref(null)
    const loginResult = ref(null)
    
    const testCredentials = reactive({
      username: 'admin',
      password: 'admin'
    })
    
    const frontendUrl = ref(window.location.origin)
    const apiUrl = ref('http://127.0.0.1:5000/api')
    const userAgent = ref(navigator.userAgent)
    
    const testHealth = async () => {
      loading.value = true
      healthResult.value = null
      
      try {
        const response = await api.get('/health')
        healthResult.value = {
          success: true,
          message: response.data.message,
          timestamp: response.data.timestamp
        }
      } catch (error) {
        console.error('健康检查失败:', error)
        healthResult.value = {
          success: false,
          message: error.message || '连接失败',
          timestamp: new Date().toISOString()
        }
      } finally {
        loading.value = false
      }
    }
    
    const testLogin = async () => {
      loading.value = true
      loginResult.value = null
      
      try {
        const response = await authAPI.login(testCredentials)
        loginResult.value = {
          success: response.data.success,
          message: response.data.message,
          user: response.data.user
        }
      } catch (error) {
        console.error('登录测试失败:', error)
        loginResult.value = {
          success: false,
          message: error.response?.data?.message || error.message || '登录失败'
        }
      } finally {
        loading.value = false
      }
    }
    
    // 页面加载时自动测试健康检查
    onMounted(() => {
      testHealth()
    })
    
    return {
      loading,
      healthResult,
      loginResult,
      testCredentials,
      frontendUrl,
      apiUrl,
      userAgent,
      testHealth,
      testLogin
    }
  }
}
</script>

<style scoped>
.api-test {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.card {
  margin-bottom: 1rem;
}

.alert {
  margin-top: 1rem;
}
</style> 