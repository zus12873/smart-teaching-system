<template>
  <div class="course-detail">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1><i class="bi bi-book me-2"></i>{{ course.name }}</h1>
          <p class="text-muted">{{ course.description || '暂无课程描述' }}</p>
        </div>
        <div>
          <router-link to="/student/dashboard" class="btn btn-outline-secondary">
            <i class="bi bi-arrow-left me-1"></i>返回主页
          </router-link>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
      <p class="mt-2">正在加载课程信息...</p>
    </div>

    <!-- 课程信息和统计 -->
    <div v-else>
      <div class="row mb-4">
        <!-- 课程基本信息 -->
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0"><i class="bi bi-info-circle me-2"></i>课程信息</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-sm-4"><strong>课程名称:</strong></div>
                <div class="col-sm-8">{{ course.name }}</div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-4"><strong>授课教师:</strong></div>
                <div class="col-sm-8">{{ course.teacher_name }}</div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-4"><strong>选课时间:</strong></div>
                <div class="col-sm-8">{{ formatDate(course.enrollment_date) }}</div>
              </div>
              <hr>
              <div class="row">
                <div class="col-sm-4"><strong>课程描述:</strong></div>
                <div class="col-sm-8">{{ course.description || '暂无描述' }}</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 学习统计 -->
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0"><i class="bi bi-bar-chart me-2"></i>学习统计</h5>
            </div>
            <div class="card-body">
              <div class="row text-center">
                <div class="col-6">
                  <div class="stat-item">
                    <h3 class="text-primary">{{ statistics.total_assignments }}</h3>
                    <p class="text-muted">总作业数</p>
                  </div>
                </div>
                <div class="col-6">
                  <div class="stat-item">
                    <h3 class="text-success">{{ statistics.completed_assignments }}</h3>
                    <p class="text-muted">已完成</p>
                  </div>
                </div>
              </div>
              <hr>
              <div class="row text-center">
                <div class="col-6">
                  <div class="stat-item">
                    <h3 class="text-warning">{{ statistics.pending_assignments }}</h3>
                    <p class="text-muted">待完成</p>
                  </div>
                </div>
                <div class="col-6">
                  <div class="stat-item">
                    <h3 :class="getCompletionRateClass()">{{ statistics.completion_rate }}%</h3>
                    <p class="text-muted">完成率</p>
                  </div>
                </div>
              </div>
              <hr v-if="statistics.average_score !== null">
              <div v-if="statistics.average_score !== null" class="text-center">
                <div class="stat-item">
                  <h3 :class="getAverageScoreClass()">{{ statistics.average_score }}</h3>
                  <p class="text-muted">平均分</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 作业列表 -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0"><i class="bi bi-file-earmark-text me-2"></i>课程作业</h5>
          <div class="btn-group" role="group">
            <button 
              type="button" 
              class="btn btn-sm" 
              :class="filterStatus === 'all' ? 'btn-primary' : 'btn-outline-primary'"
              @click="filterStatus = 'all'">
              全部 ({{ assignments.length }})
            </button>
            <button 
              type="button" 
              class="btn btn-sm" 
              :class="filterStatus === 'pending' ? 'btn-warning' : 'btn-outline-warning'"
              @click="filterStatus = 'pending'">
              待完成 ({{ statistics.pending_assignments }})
            </button>
            <button 
              type="button" 
              class="btn btn-sm" 
              :class="filterStatus === 'completed' ? 'btn-success' : 'btn-outline-success'"
              @click="filterStatus = 'completed'">
              已完成 ({{ statistics.completed_assignments }})
            </button>
          </div>
        </div>
        <div class="card-body">
          <div v-if="filteredAssignments.length > 0">
            <div class="assignment-item" v-for="assignment in filteredAssignments" :key="assignment.id">
              <div class="assignment-info">
                <h6>{{ assignment.title }}</h6>
                <p class="text-muted" v-if="assignment.description">{{ assignment.description }}</p>
                <div class="assignment-meta">
                  <span class="badge bg-secondary me-2">
                    <i class="bi bi-list-task me-1"></i>
                    {{ assignment.problems_count }}题
                  </span>
                  <span v-if="assignment.due_date" class="badge me-2" :class="getDeadlineBadgeClass(assignment.due_date)">
                    <i class="bi bi-calendar me-1"></i>
                    {{ formatDueDate(assignment.due_date) }}
                  </span>
                  <span class="badge" :class="getStatusBadgeClass(assignment.status)">
                    <i class="bi" :class="getStatusIcon(assignment.status)"></i>
                    {{ getStatusText(assignment.status) }}
                  </span>
                  <span v-if="assignment.total_score !== undefined && assignment.is_graded" 
                        class="badge ms-2" :class="getScoreBadgeClass(assignment.total_score)">
                    {{ assignment.total_score }}分
                  </span>
                </div>
              </div>
              <div class="assignment-actions">
                <button class="btn btn-sm" 
                        :class="assignment.status === 'completed' ? 'btn-outline-primary' : 'btn-primary'"
                        @click="viewAssignment(assignment.id)">
                  {{ assignment.status === 'completed' ? '查看详情' : '开始作业' }}
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-center text-muted py-4">
            <i class="bi bi-inbox display-4 mb-3"></i>
            <h5>暂无作业</h5>
            <p v-if="filterStatus === 'all'">该课程还没有布置作业</p>
            <p v-else-if="filterStatus === 'pending'">当前没有待完成的作业</p>
            <p v-else>还没有完成任何作业</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../utils/api'

export default {
  name: 'StudentCourseDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const isLoading = ref(true)
    const course = ref({})
    const assignments = ref([])
    const statistics = ref({})
    const filterStatus = ref('all')

    // 计算属性
    const filteredAssignments = computed(() => {
      if (filterStatus.value === 'all') {
        return assignments.value
      }
      return assignments.value.filter(assignment => assignment.status === filterStatus.value)
    })

    // 加载课程详情
    const loadCourseDetail = async () => {
      try {
        isLoading.value = true
        const courseId = route.params.id
        const response = await api.get(`/student/courses/${courseId}`)
        
        if (response.data.success) {
          const data = response.data.data
          course.value = data.course
          assignments.value = data.assignments
          statistics.value = data.statistics
        } else {
          throw new Error(response.data.message || '加载失败')
        }
      } catch (error) {
        console.error('加载课程详情失败:', error)
        alert('加载课程详情失败: ' + error.message)
        router.push('/student/dashboard')
      } finally {
        isLoading.value = false
      }
    }

    // 辅助方法
    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      return new Date(dateString).toLocaleDateString('zh-CN')
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

    const getStatusBadgeClass = (status) => {
      return status === 'completed' ? 'bg-success' : 'bg-warning'
    }

    const getStatusIcon = (status) => {
      return status === 'completed' ? 'bi-check-circle me-1' : 'bi-clock me-1'
    }

    const getStatusText = (status) => {
      return status === 'completed' ? '已完成' : '待完成'
    }

    const getScoreBadgeClass = (score) => {
      if (score >= 80) return 'bg-success'
      if (score >= 60) return 'bg-warning'
      return 'bg-danger'
    }

    const getCompletionRateClass = () => {
      const rate = statistics.value.completion_rate
      if (rate >= 80) return 'text-success'
      if (rate >= 60) return 'text-warning'
      return 'text-danger'
    }

    const getAverageScoreClass = () => {
      const score = statistics.value.average_score
      if (score >= 80) return 'text-success'
      if (score >= 60) return 'text-warning'
      return 'text-danger'
    }

    const viewAssignment = (assignmentId) => {
      router.push(`/student/assignment/${assignmentId}`)
    }

    onMounted(() => {
      loadCourseDetail()
    })

    return {
      isLoading,
      course,
      assignments,
      statistics,
      filterStatus,
      filteredAssignments,
      loadCourseDetail,
      formatDate,
      formatDueDate,
      getDeadlineBadgeClass,
      getStatusBadgeClass,
      getStatusIcon,
      getStatusText,
      getScoreBadgeClass,
      getCompletionRateClass,
      getAverageScoreClass,
      viewAssignment
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
  font-weight: 600;
}

.stat-item {
  padding: 0.5rem 0;
}

.stat-item h3 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
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
  margin-right: 0.25rem;
}

.btn-group .btn {
  border-radius: 0.375rem;
  margin-right: 0.25rem;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header .d-flex {
    flex-direction: column;
    align-items: flex-start !important;
  }
  
  .page-header .btn {
    margin-top: 1rem;
  }
  
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
  
  .btn-group {
    display: flex;
    flex-wrap: wrap;
  }
  
  .btn-group .btn {
    flex: 1;
    margin-bottom: 0.25rem;
  }
}
</style> 