<template>
  <div class="student-dashboard">
    <div class="page-header">
      <h1><i class="bi bi-mortarboard me-2"></i>学生学习中心</h1>
      <p>欢迎回来，{{ user.username }}同学</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载仪表板数据...</p>
    </div>

    <!-- 学习进度总览 -->
    <div v-else>
      <div class="row mb-4">
        <div class="col-md-3">
          <div class="card stat-card">
            <div class="card-body">
              <div class="stat-icon">
                <i class="bi bi-book"></i>
              </div>
              <div class="stat-content">
                <h3>{{ dashboardData.stats.courses_count }}</h3>
                <p>已选课程</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-3">
          <div class="card stat-card">
            <div class="card-body">
              <div class="stat-icon">
                <i class="bi bi-file-earmark-text"></i>
              </div>
              <div class="stat-content">
                <h3>{{ totalAssignments }}</h3>
                <p>总作业数</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-3">
          <div class="card stat-card">
            <div class="card-body">
              <div class="stat-icon">
                <i class="bi bi-check-circle"></i>
              </div>
              <div class="stat-content">
                <h3>{{ dashboardData.stats.completed_count }}</h3>
                <p>已完成</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-3">
          <div class="card stat-card">
            <div class="card-body">
              <div class="stat-icon">
                <i class="bi bi-clock"></i>
              </div>
              <div class="stat-content">
                <h3>{{ dashboardData.stats.pending_count }}</h3>
                <p>待完成</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 待完成作业 -->
      <div class="row">
        <div class="col-md-8">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">待完成作业</h5>
              <span class="badge bg-primary">{{ dashboardData.pending_assignments.length }}</span>
            </div>
            <div class="card-body">
              <div v-if="dashboardData.pending_assignments.length > 0">
                <div class="assignment-item" v-for="assignment in dashboardData.pending_assignments" :key="assignment.id">
                  <div class="assignment-info">
                    <h6>{{ assignment.title }}</h6>
                    <p class="text-muted">
                      <small>课程: {{ assignment.course_name }}</small>
                    </p>
                    <div class="assignment-meta">
                      <span class="badge" :class="getDeadlineBadgeClass(assignment.due_date)">
                        <i class="bi bi-calendar me-1"></i>
                        {{ formatDueDate(assignment.due_date) }}
                      </span>
                      <span class="badge bg-info ms-2">
                        <i class="bi bi-list-task me-1"></i>
                        {{ assignment.problems_count }}题
                      </span>
                    </div>
                  </div>
                  <div class="assignment-actions">
                    <button class="btn btn-sm btn-primary" @click="viewAssignment(assignment.id)">
                      开始作业
                    </button>
                  </div>
                </div>
              </div>
              <div v-else class="text-center text-muted py-4">
                <i class="bi bi-check-circle display-4 mb-3 text-success"></i>
                <h5>太棒了！</h5>
                <p>当前没有待完成的作业</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="card mb-3">
            <div class="card-header">
              <h5 class="mb-0">我的课程</h5>
            </div>
            <div class="card-body">
              <div v-if="dashboardData.courses.length > 0">
                <div class="course-item" v-for="course in dashboardData.courses" :key="course.id">
                  <div class="course-info">
                    <h6>{{ course.name }}</h6>
                    <p class="text-muted">{{ course.teacher_name }}</p>
                    <small class="text-muted">{{ course.assignments_count }}个作业</small>
                  </div>
                  <button class="btn btn-sm btn-outline-primary" @click="viewCourse(course.id)">
                    查看
                  </button>
                </div>
              </div>
              <div v-else class="text-center text-muted">
                <i class="bi bi-inbox display-4 mb-3"></i>
                <p>还没有选修课程</p>
              </div>
            </div>
          </div>
          
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">快速操作</h5>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <button class="btn btn-outline-primary" @click="viewAllAssignments">
                  <i class="bi bi-list me-2"></i>所有作业
                </button>
                <button class="btn btn-outline-success" @click="viewGrades">
                  <i class="bi bi-bar-chart me-2"></i>我的成绩
                </button>
                <button class="btn btn-outline-info" @click="viewSchedule">
                  <i class="bi bi-calendar me-2"></i>课程表
                </button>
                <router-link to="/profile" class="btn btn-outline-secondary">
                  <i class="bi bi-person-gear me-2"></i>个人设置
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近提交的作业 -->
      <div class="row mt-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">最近提交</h5>
            </div>
            <div class="card-body">
              <div v-if="dashboardData.completed_assignments.length > 0" class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>作业名称</th>
                      <th>课程</th>
                      <th>提交时间</th>
                      <th>状态</th>
                      <th>成绩</th>
                      <th>操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="assignment in dashboardData.completed_assignments.slice(0, 5)" :key="assignment.id">
                      <td>{{ assignment.title }}</td>
                      <td>{{ assignment.course_name }}</td>
                      <td>{{ formatDate(assignment.submitted_at) }}</td>
                      <td>
                        <span class="badge" :class="getStatusBadgeClass(assignment.is_graded)">
                          {{ assignment.is_graded ? '已批改' : '已提交' }}
                        </span>
                      </td>
                      <td>
                        <span v-if="assignment.total_score !== null" class="fw-bold" :class="getScoreClass(assignment.total_score)">
                          {{ assignment.total_score }}
                        </span>
                        <span v-else class="text-muted">待评分</span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-outline-primary" @click="viewAssignment(assignment.id)">
                          查看
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center text-muted py-4">
                <i class="bi bi-file-earmark display-4 mb-3"></i>
                <p>还没有提交任何作业</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 开发提示 -->
    <div class="alert alert-info mt-4">
      <i class="bi bi-info-circle me-2"></i>
      欢迎使用智能教学系统学生端，开始您的学习之旅吧！
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { user } from '../../stores/auth'
import api from '../../utils/api'

export default {
  name: 'StudentDashboard',
  setup() {
    const router = useRouter()
    const dashboardData = ref({
      courses: [],
      pending_assignments: [],
      completed_assignments: [],
      stats: {
        courses_count: 0,
        pending_count: 0,
        completed_count: 0
      }
    })
    const isLoading = ref(true)

    // 计算属性
    const totalAssignments = computed(() => {
      return dashboardData.value.stats.pending_count + dashboardData.value.stats.completed_count
    })

    const loadDashboardData = async () => {
      try {
        isLoading.value = true
        const response = await api.get('/student/dashboard')
        
        if (response.data.success) {
          dashboardData.value = response.data.data
        } else {
          throw new Error(response.data.message || '加载失败')
        }
      } catch (error) {
        console.error('加载学生仪表板数据失败:', error)
        // 显示错误提示，但不重定向
        alert('加载仪表板数据失败，请刷新页面重试')
      } finally {
        isLoading.value = false
      }
    }

    const formatDueDate = (dateString) => {
      if (!dateString) return '无截止日期'
      
      const date = new Date(dateString)
      const now = new Date()
      const diffTime = date - now
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays < 0) {
        return '已过期'
      } else if (diffDays === 0) {
        return '今天截止'
      } else if (diffDays === 1) {
        return '明天截止'
      } else {
        return `${diffDays}天后截止`
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    const getDeadlineBadgeClass = (dueDate) => {
      if (!dueDate) return 'bg-secondary'
      
      const date = new Date(dueDate)
      const now = new Date()
      const diffTime = date - now
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays < 0) {
        return 'bg-danger'
      } else if (diffDays <= 1) {
        return 'bg-warning'
      } else {
        return 'bg-primary'
      }
    }

    const getStatusBadgeClass = (isGraded) => {
      return isGraded ? 'bg-success' : 'bg-info'
    }

    const getScoreClass = (score) => {
      if (score >= 80) return 'text-success'
      if (score >= 60) return 'text-warning'
      return 'text-danger'
    }

    const viewAssignment = (assignmentId) => {
      router.push(`/student/assignment/${assignmentId}`)
    }

    const viewCourse = (courseId) => {
      router.push(`/student/course/${courseId}`)
    }

    const viewAllAssignments = () => {
      // 这里可以实现所有作业列表页面
      alert('查看所有作业功能开发中...')
    }

    const viewGrades = () => {
      // 这里可以实现成绩查看页面
      alert('查看成绩功能开发中...')
    }

    const viewSchedule = () => {
      // 这里可以实现课程表页面
      alert('查看课程表功能开发中...')
    }

    onMounted(() => {
      loadDashboardData()
    })

    return {
      user,
      dashboardData,
      totalAssignments,
      isLoading,
      formatDueDate,
      formatDate,
      getDeadlineBadgeClass,
      getStatusBadgeClass,
      getScoreClass,
      viewAssignment,
      viewCourse,
      viewAllAssignments,
      viewGrades,
      viewSchedule
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

.stat-card {
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-bottom: 1rem;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-card .card-body {
  display: flex;
  align-items: center;
  padding: 1.5rem;
}

.stat-icon {
  font-size: 2.5rem;
  margin-right: 1rem;
  opacity: 0.8;
}

.stat-content h3 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.stat-content p {
  margin-bottom: 0;
  opacity: 0.9;
}

.assignment-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  transition: all 0.2s;
}

.assignment-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-color: #007bff;
}

.assignment-info h6 {
  margin-bottom: 0.5rem;
  color: #495057;
}

.assignment-meta {
  margin-top: 0.5rem;
}

.assignment-meta .badge {
  margin-right: 0.5rem;
}

.course-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  border: 1px solid #e9ecef;
  border-radius: 0.375rem;
  margin-bottom: 0.75rem;
}

.course-item:hover {
  background-color: #f8f9fa;
}

.course-info h6 {
  margin-bottom: 0.25rem;
  color: #495057;
}

.course-info p {
  margin-bottom: 0.25rem;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.card-header {
  background-color: #f8f9fa !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
}

.badge {
  font-size: 0.8em;
}

.alert-info {
  border-color: #b3d7ff;
  background-color: #e7f3ff;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .assignment-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .assignment-actions {
    margin-top: 1rem;
    width: 100%;
  }
  
  .assignment-actions .btn {
    width: 100%;
  }
  
  .course-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .course-item .btn {
    margin-top: 0.5rem;
    width: 100%;
  }
  
  .stat-card .card-body {
    flex-direction: column;
    text-align: center;
  }
  
  .stat-icon {
    margin-right: 0;
    margin-bottom: 1rem;
  }
}
</style> 