<template>
  <div class="admin-dashboard">
    <div class="page-header">
      <h1><i class="bi bi-speedometer me-2"></i>管理员面板</h1>
      <p>系统概览与管理</p>
    </div>

    <!-- 统计卡片 -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <i class="bi bi-people-fill fs-1 text-primary mb-3"></i>
            <h5 class="card-title">教师总数</h5>
            <p class="card-text display-6">{{ stats.teacherCount }}</p>
            <router-link to="/admin/users" class="btn btn-sm btn-primary">管理教师</router-link>
          </div>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <i class="bi bi-mortarboard-fill fs-1 text-success mb-3"></i>
            <h5 class="card-title">学生总数</h5>
            <p class="card-text display-6">{{ stats.studentCount }}</p>
            <router-link to="/admin/users" class="btn btn-sm btn-success">管理学生</router-link>
          </div>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <i class="bi bi-journal-album fs-1 text-info mb-3"></i>
            <h5 class="card-title">课程总数</h5>
            <p class="card-text display-6">{{ stats.courseCount }}</p>
            <router-link to="/admin/courses" class="btn btn-sm btn-info">管理课程</router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近数据 -->
    <div class="row mt-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-light">
            <h5 class="mb-0">最近添加的教师</h5>
          </div>
          <div class="card-body">
            <div v-if="recentTeachers.length > 0" class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>用户名</th>
                    <th>邮箱</th>
                    <th>添加时间</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="teacher in recentTeachers" :key="teacher.id">
                    <td>{{ teacher.username }}</td>
                    <td>{{ teacher.email }}</td>
                    <td>{{ formatDate(teacher.created_at) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p v-else class="text-muted">暂无教师数据</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-light">
            <h5 class="mb-0">最近添加的课程</h5>
          </div>
          <div class="card-body">
            <div v-if="recentCourses.length > 0" class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>课程名称</th>
                    <th>授课教师</th>
                    <th>添加时间</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="course in recentCourses" :key="course.id">
                    <td>{{ course.name }}</td>
                    <td>{{ course.teacher?.username }}</td>
                    <td>{{ formatDate(course.created_at) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p v-else class="text-muted">暂无课程数据</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="mt-4">
      <div class="card">
        <div class="card-header bg-light">
          <h5 class="mb-0">系统快捷操作</h5>
        </div>
        <div class="card-body">
          <div class="row text-center">
            <div class="col-md-4 mb-3">
              <router-link to="/admin/users" class="btn btn-outline-primary btn-lg w-100">
                <i class="bi bi-person-plus-fill me-2"></i>添加新用户
              </router-link>
            </div>
            <div class="col-md-4 mb-3">
              <router-link to="/admin/courses" class="btn btn-outline-success btn-lg w-100">
                <i class="bi bi-journal-plus me-2"></i>创建新课程
              </router-link>
            </div>
            <div class="col-md-4 mb-3">
              <button class="btn btn-outline-secondary btn-lg w-100" @click="openSettings">
                <i class="bi bi-gear-fill me-2"></i>系统设置
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../../utils/api'

export default {
  name: 'AdminDashboard',
  setup() {
    const stats = ref({
      teacherCount: 0,
      studentCount: 0,
      courseCount: 0
    })
    
    const recentTeachers = ref([])
    const recentCourses = ref([])

    const loadDashboardData = async (retryCount = 0) => {
      try {
        // 使用后端的dashboard端点获取所有数据
        const response = await api.get('/admin/dashboard')
        const data = response.data.data
        
        // 设置统计数据
        stats.value = {
          teacherCount: data.stats.teachers_count,
          studentCount: data.stats.students_count,
          courseCount: data.stats.courses_count
        }
        
        // 设置最近的教师和课程
        recentTeachers.value = data.recent_teachers
        recentCourses.value = data.recent_courses
      } catch (error) {
        console.error('加载仪表板数据失败:', error)
        
        // 如果是401错误且还没重试过，则稍后重试一次
        if (error.response?.status === 401 && retryCount < 2) {
          console.log(`第${retryCount + 1}次重试加载仪表板数据...`)
          setTimeout(() => {
            loadDashboardData(retryCount + 1)
          }, 500 * (retryCount + 1)) // 递增延迟
          return
        }
        
        // 使用模拟数据
        stats.value = {
          teacherCount: 12,
          studentCount: 156,
          courseCount: 8
        }
        recentTeachers.value = [
          { id: 1, username: '张老师', email: 'zhang@example.com', created_at: '2024-01-15' },
          { id: 2, username: '李老师', email: 'li@example.com', created_at: '2024-01-14' }
        ]
        recentCourses.value = [
          { id: 1, name: '高等数学', teacher: { username: '张老师' }, created_at: '2024-01-15' },
          { id: 2, name: '线性代数', teacher: { username: '李老师' }, created_at: '2024-01-14' }
        ]
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    const openSettings = () => {
      alert('系统设置功能开发中...')
    }

    onMounted(() => {
      loadDashboardData()
    })

    return {
      stats,
      recentTeachers,
      recentCourses,
      formatDate,
      openSettings
    }
  }
}
</script>

<style scoped>
.page-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.page-header h1 {
  color: #495057;
  font-weight: 600;
}

.page-header p {
  color: #6c757d;
  margin-bottom: 0;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.card-header {
  background-color: #f8f9fa !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.display-6 {
  font-size: 2.5rem;
  font-weight: 600;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
}

.btn-lg {
  padding: 0.75rem 1.5rem;
}
</style> 