<template>
  <div class="create-assignment">
    <div class="page-header">
      <h1><i class="bi bi-file-earmark-plus me-2"></i>创建新作业</h1>
      <p>为您的课程创建新的作业</p>
    </div>

    <div class="row">
      <div class="col-md-8 mx-auto">
        <div class="card">
          <div class="card-header bg-light">
            <h5 class="mb-0">作业信息</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="createAssignment">
              <div class="mb-3">
                <label for="title" class="form-label">作业标题</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="title" 
                  v-model="formData.title"
                  required
                  placeholder="请输入作业标题"
                >
              </div>
              
              <div class="mb-3">
                <label for="course_id" class="form-label">所属课程</label>
                <select 
                  class="form-select" 
                  id="course_id" 
                  v-model="formData.course_id"
                  required
                >
                  <option value="" disabled>请选择课程</option>
                  <option 
                    v-for="course in courses" 
                    :key="course.id" 
                    :value="course.id"
                  >
                    {{ course.name }}
                  </option>
                </select>
              </div>
              
              <div class="mb-3">
                <label for="description" class="form-label">作业描述</label>
                <textarea 
                  class="form-control" 
                  id="description" 
                  v-model="formData.description"
                  rows="4"
                  placeholder="描述作业的要求、目标和注意事项"
                ></textarea>
                <div class="form-text">描述作业的要求、目标和注意事项</div>
              </div>
              
              <div class="mb-3">
                <label for="due_date" class="form-label">截止日期（可选）</label>
                <input 
                  type="date" 
                  class="form-control" 
                  id="due_date" 
                  v-model="formData.due_date"
                >
              </div>
              
              <div class="d-grid gap-2">
                <button 
                  type="submit" 
                  class="btn btn-primary"
                  :disabled="isSubmitting"
                >
                  <i class="bi bi-plus-circle me-1"></i>
                  {{ isSubmitting ? '创建中...' : '创建作业' }}
                </button>
                <router-link to="/teacher/dashboard" class="btn btn-outline-secondary">
                  <i class="bi bi-x-circle me-1"></i>取消
                </router-link>
              </div>
            </form>
          </div>
        </div>
        
        <div class="card mt-4">
          <div class="card-header bg-light">
            <h5 class="mb-0">作业创建说明</h5>
          </div>
          <div class="card-body">
            <p>创建作业的步骤：</p>
            <ol>
              <li>填写作业的基本信息并选择所属课程</li>
              <li>点击"创建作业"按钮提交</li>
              <li>系统将引导您添加作业题目</li>
              <li>您可以：
                <ul>
                  <li>手动编写题目</li>
                  <li>使用智能出题系统自动生成题目</li>
                  <li>上传题库导入题目</li>
                </ul>
              </li>
            </ol>
            <div class="alert alert-info">
              <i class="bi bi-info-circle me-1"></i>提示：创建作业后，您可以随时编辑作业内容和题目。
            </div>
          </div>
        </div>

        <!-- 智能助手卡片 -->
        <div class="card mt-4">
          <div class="card-header bg-light">
            <h5 class="mb-0">智能创建助手</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3">
                <div class="card h-100 assistant-card">
                  <div class="card-body text-center">
                    <i class="bi bi-lightbulb-fill fs-1 text-warning mb-3"></i>
                    <h5 class="card-title">智能出题</h5>
                    <p class="card-text">创建作业后，可使用AI自动生成题目</p>
                    <router-link to="/problem-generation" class="btn btn-outline-warning">
                      前往出题
                    </router-link>
                  </div>
                </div>
              </div>
              
              <div class="col-md-6 mb-3">
                <div class="card h-100 assistant-card">
                  <div class="card-body text-center">
                    <i class="bi bi-upload fs-1 text-success mb-3"></i>
                    <h5 class="card-title">智能批改</h5>
                    <p class="card-text">创建后可设置AI自动批改功能</p>
                    <router-link to="/multi-upload" class="btn btn-outline-success">
                      了解批改
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { teacherAPI } from '../../utils/api'

export default {
  name: 'CreateAssignment',
  setup() {
    const router = useRouter()
    const route = useRoute()
    
    const courses = ref([])
    const isLoading = ref(true)
    const isSubmitting = ref(false)
    
    const formData = ref({
      title: '',
      course_id: '',
      description: '',
      due_date: ''
    })

    const loadCourses = async () => {
      try {
        const response = await teacherAPI.getCourses()
        if (response.data.success) {
          courses.value = response.data.courses
          
          // 如果URL中有course参数，自动选择该课程
          const courseParam = route.query.course
          if (courseParam) {
            formData.value.course_id = courseParam
          }
        } else {
          throw new Error(response.data.message || '加载课程列表失败')
        }
      } catch (error) {
        console.error('加载课程列表失败:', error)
        alert('加载课程列表失败，请稍后重试')
      } finally {
        isLoading.value = false
      }
    }

    const createAssignment = async () => {
      // 防重复提交检查
      if (isSubmitting.value) {
        console.log('正在创建作业中，请勿重复提交')
        return
      }
      
      if (!formData.value.title.trim()) {
        alert('请输入作业标题')
        return
      }
      
      if (!formData.value.course_id) {
        alert('请选择所属课程')
        return
      }

      isSubmitting.value = true
      
      try {
        const response = await teacherAPI.createAssignment({
          title: formData.value.title.trim(),
          course_id: formData.value.course_id,
          description: formData.value.description.trim() || null,
          due_date: formData.value.due_date || null
        })
        
        if (response.data.success) {
          const assignmentId = response.data.assignment.id
          alert('作业创建成功！现在您可以为作业添加题目。')
          // 跳转到编辑作业页面
          router.push(`/teacher/assignments/${assignmentId}/edit`)
        } else {
          throw new Error(response.data.message || '创建作业失败')
        }
      } catch (error) {
        console.error('创建作业失败:', error)
        alert(error.response?.data?.message || '创建作业失败，请稍后重试')
      } finally {
        isSubmitting.value = false
      }
    }

    const setMinDate = () => {
      // 设置最小日期为今天
      const today = new Date().toISOString().split('T')[0]
      const dueDateInput = document.getElementById('due_date')
      if (dueDateInput) {
        dueDateInput.min = today
      }
    }

    onMounted(() => {
      loadCourses()
      setMinDate()
    })

    return {
      courses,
      formData,
      isLoading,
      isSubmitting,
      createAssignment
    }
  }
}
</script>

<style scoped>
/* 全局容器样式 */
.create-assignment {
  max-width: 1600px;
  margin: 0 auto;
  padding: 1.5rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: #f8fafc;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  margin-bottom: 2rem;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  border-left: 4px solid #3b82f6;
}

.page-header h1 {
  color: #1f2937;
  font-weight: 700;
  font-size: 2.25rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-header p {
  color: #6b7280;
  margin-bottom: 0;
  font-size: 1.125rem;
}

/* 主要内容区域布局 */
.row {
  margin: 0 -0.75rem;
}

.col-md-8 {
  padding: 0 0.75rem;
  max-width: none;
  flex: 1;
}

/* 卡片样式 */
.card {
  border: none;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.card-header {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
  font-weight: 600;
  padding: 1.5rem;
  color: #1f2937;
  font-size: 1.125rem;
}

.card-body {
  padding: 2rem;
}

/* 表单样式 */
.form-label {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.form-control,
.form-select {
  border-radius: 10px;
  border: 2px solid #e5e7eb;
  padding: 0.875rem 1rem;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background: white;
}

.form-control:focus,
.form-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  outline: none;
}

.form-text {
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

/* 按钮样式 */
.btn {
  border-radius: 10px;
  font-weight: 600;
  padding: 0.875rem 1.5rem;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.39);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5);
  color: white;
}

.btn-outline-secondary {
  background: white;
  color: #6b7280;
  border: 2px solid #d1d5db;
}

.btn-outline-secondary:hover {
  background: #f3f4f6;
  color: #374151;
  border-color: #9ca3af;
  transform: translateY(-1px);
}

.d-grid {
  gap: 1rem;
}

/* 智能助手卡片 */
.assistant-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border-radius: 16px;
  overflow: hidden;
  position: relative;
}

.assistant-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-color, #3b82f6), var(--accent-color-dark, #2563eb));
}

.assistant-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.assistant-card .card-body {
  padding: 2rem 1.5rem;
  text-align: center;
}

.assistant-card .fs-1 {
  font-size: 3rem !important;
  margin-bottom: 1.5rem;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.assistant-card h5 {
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.assistant-card p {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.btn-outline-warning {
  --accent-color: #f59e0b;
  --accent-color-dark: #d97706;
  background: white;
  color: #f59e0b;
  border: 2px solid #f59e0b;
}

.btn-outline-warning:hover {
  background: #f59e0b;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4);
}

.btn-outline-success {
  --accent-color: #10b981;
  --accent-color-dark: #059669;
  background: white;
  color: #10b981;
  border: 2px solid #10b981;
}

.btn-outline-success:hover {
  background: #10b981;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}

/* 说明卡片 */
.alert {
  border-radius: 12px;
  border: none;
  padding: 1rem 1.5rem;
  background: #eff6ff;
  color: #1e40af;
  border-left: 4px solid #3b82f6;
}

/* 列表样式 */
ol {
  padding-left: 1.5rem;
}

ol li {
  margin-bottom: 0.75rem;
  line-height: 1.6;
}

ul {
  margin-top: 0.5rem;
  padding-left: 1.5rem;
}

ul li {
  margin-bottom: 0.5rem;
}

/* 加载状态 */
.loading-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  background: white;
  border-radius: 16px;
  margin: 2rem 0;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .create-assignment {
    max-width: 1200px;
    padding: 1.25rem;
  }
}

@media (max-width: 1024px) {
  .create-assignment {
    padding: 1rem;
  }
  
  .page-header {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  .create-assignment {
    padding: 0.75rem;
  }
  
  .col-md-8 {
    padding: 0 0.375rem;
  }
  
  .row {
    margin: 0 -0.375rem;
  }
  
  .card-body {
    padding: 1.5rem;
  }
  
  .assistant-card .card-body {
    padding: 1.5rem 1rem;
  }
  
  .assistant-card .fs-1 {
    font-size: 2.5rem !important;
  }
  
  .page-header {
    padding: 1.25rem;
  }
  
  .page-header h1 {
    font-size: 1.75rem;
  }
}

@media (max-width: 576px) {
  .create-assignment {
    padding: 0.5rem;
  }
  
  .page-header {
    padding: 1rem;
    margin-bottom: 1rem;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .card-body {
    padding: 1rem;
  }
  
  .btn {
    padding: 0.75rem 1.25rem;
    font-size: 0.9rem;
  }
}
</style>
