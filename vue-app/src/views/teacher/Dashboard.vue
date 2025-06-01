<template>
  <div class="teacher-dashboard">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1><i class="bi bi-house-door me-3"></i>教师工作台</h1>
          <p class="header-subtitle">欢迎回来，{{ user?.username || '教师' }}老师</p>
        </div>
        <div class="header-time">
          <div class="time-card">
            <i class="bi bi-calendar3 me-2"></i>
            <span>{{ currentDate }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷功能卡片 -->
    <div class="quick-actions-section">
      <h2 class="section-title">
        <i class="bi bi-lightning-charge me-2"></i>智能教学工具
      </h2>
      <div class="row g-4">
        <div class="col-lg-4 col-md-6">
          <div class="action-card gradient-warning">
            <div class="card-icon">
              <i class="bi bi-lightbulb-fill"></i>
            </div>
            <div class="card-content">
              <h5>智能出题</h5>
              <p>AI驱动的题目生成系统，快速创建高质量试题</p>
              <router-link to="/problem-generation" class="btn btn-custom btn-warning">
                <i class="bi bi-plus-circle me-2"></i>开始出题
              </router-link>
            </div>
          </div>
        </div>
        
        <div class="col-lg-4 col-md-6">
          <div class="action-card gradient-success">
            <div class="card-icon">
              <i class="bi bi-robot"></i>
            </div>
            <div class="card-content">
              <h5>智能批改</h5>
              <p>自动化批改系统，提升批改效率和准确性</p>
              <router-link to="/multi-upload" class="btn btn-custom btn-success">
                <i class="bi bi-upload me-2"></i>开始批改
              </router-link>
            </div>
          </div>
        </div>
        
        <div class="col-lg-4 col-md-6">
          <div class="action-card gradient-info">
            <div class="card-icon">
              <i class="bi bi-journal-bookmark"></i>
            </div>
            <div class="card-content">
              <h5>课程管理</h5>
              <p>全面管理您的课程、学生和教学资源</p>
              <button class="btn btn-custom btn-info" @click="viewCourses">
                <i class="bi bi-arrow-right me-2"></i>进入管理
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="stats-section" v-if="!isLoading">
      <h2 class="section-title">
        <i class="bi bi-graph-up me-2"></i>数据统计
      </h2>
      <div class="row g-4">
        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-primary">
            <div class="stat-icon">
              <i class="bi bi-journal-album"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats?.coursesCount || 0 }}</div>
              <div class="stat-label">我的课程</div>
              <div class="stat-trend">
                <i class="bi bi-arrow-up"></i>
                <span>较上月</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-success">
            <div class="stat-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats?.assignmentsCount || 0 }}</div>
              <div class="stat-label">作业总数</div>
              <div class="stat-trend">
                <i class="bi bi-arrow-up"></i>
                <span>本学期</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-info">
            <div class="stat-icon">
              <i class="bi bi-people"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats?.studentsCount || 0 }}</div>
              <div class="stat-label">学生总数</div>
              <div class="stat-trend">
                <i class="bi bi-dash"></i>
                <span>活跃用户</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-warning">
            <div class="stat-icon">
              <i class="bi bi-clipboard-check"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ pendingSubmissions }}</div>
              <div class="stat-label">待批改</div>
              <div class="stat-trend">
                <i class="bi bi-exclamation-triangle"></i>
                <span>需处理</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-section">
      <div class="loading-card">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">加载中...</span>
        </div>
        <p class="loading-text">正在加载数据...</p>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content" v-if="!isLoading">
      <div class="row g-4">
        <!-- 课程管理 -->
        <div class="col-lg-8">
          <div class="content-card">
            <div class="card-header-custom">
              <div class="d-flex justify-content-between align-items-center">
                <h3 class="card-title-custom">
                  <i class="bi bi-journal-album me-2"></i>我的课程
                </h3>
                <button class="btn btn-outline-primary btn-sm" @click="viewCourses">
                  <i class="bi bi-arrow-right me-1"></i>查看全部
                </button>
              </div>
            </div>
            <div class="card-body-custom">
              <div v-if="courses.length > 0" class="courses-grid">
                <div class="course-item" v-for="course in courses" :key="course.id">
                  <div class="course-header">
                    <div class="course-icon">
                      <i class="bi bi-book"></i>
                    </div>
                    <div class="course-info">
                      <h6 class="course-name">{{ course.name }}</h6>
                      <div class="course-meta">
                        <span class="meta-item">
                          <i class="bi bi-people me-1"></i>{{ course.students_count || 0 }}名学生
                        </span>
                        <span class="meta-item">
                          <i class="bi bi-file-text me-1"></i>{{ course.assignments_count || 0 }}个作业
                        </span>
                      </div>
                    </div>
                  </div>
                  <div class="course-actions">
                    <button class="btn btn-sm btn-outline-primary" @click="viewCourse(course.id)">
                      <i class="bi bi-eye me-1"></i>查看
                    </button>
                    <button class="btn btn-sm btn-primary" @click="createAssignment(course.id)">
                      <i class="bi bi-plus me-1"></i>布置作业
                    </button>
                  </div>
                </div>
              </div>
              <div v-else class="empty-state">
                <div class="empty-icon">
                  <i class="bi bi-journal-x"></i>
                </div>
                <h5 class="empty-title">暂无课程</h5>
                <p class="empty-description">请联系管理员为您分配课程</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 侧边栏 -->
        <div class="col-lg-4">
          <!-- 快速操作 -->
          <div class="content-card mb-4">
            <div class="card-header-custom">
              <h3 class="card-title-custom">
                <i class="bi bi-lightning me-2"></i>快速操作
              </h3>
            </div>
            <div class="card-body-custom">
              <div class="quick-actions-list">
                <button class="quick-action-item" @click="createAssignment()">
                  <div class="action-icon bg-primary">
                    <i class="bi bi-plus-circle"></i>
                  </div>
                  <div class="action-text">
                    <h6>创建作业</h6>
                    <small>为课程布置新作业</small>
                  </div>
                  <i class="bi bi-chevron-right action-arrow"></i>
                </button>
                
                <router-link to="/problem-generation" class="quick-action-item">
                  <div class="action-icon bg-warning">
                    <i class="bi bi-lightbulb"></i>
                  </div>
                  <div class="action-text">
                    <h6>智能出题</h6>
                    <small>AI生成试题</small>
                  </div>
                  <i class="bi bi-chevron-right action-arrow"></i>
                </router-link>
                
                <router-link to="/multi-upload" class="quick-action-item">
                  <div class="action-icon bg-success">
                    <i class="bi bi-robot"></i>
                  </div>
                  <div class="action-text">
                    <h6>智能批改</h6>
                    <small>自动批改作业</small>
                  </div>
                  <i class="bi bi-chevron-right action-arrow"></i>
                </router-link>
                
                <button class="quick-action-item" @click="viewAllAssignments">
                  <div class="action-icon bg-info">
                    <i class="bi bi-list-check"></i>
                  </div>
                  <div class="action-text">
                    <h6>所有作业</h6>
                    <small>查看作业列表</small>
                  </div>
                  <i class="bi bi-chevron-right action-arrow"></i>
                </button>
              </div>
            </div>
          </div>

          <!-- 最近作业 -->
          <div class="content-card">
            <div class="card-header-custom">
              <h3 class="card-title-custom">
                <i class="bi bi-clock-history me-2"></i>最近作业
              </h3>
            </div>
            <div class="card-body-custom">
              <div v-if="recentAssignments.length > 0" class="recent-assignments">
                <div class="assignment-item" v-for="assignment in recentAssignments" :key="assignment.id">
                  <div class="assignment-info">
                    <h6 class="assignment-title">{{ assignment.title }}</h6>
                    <p class="assignment-course">{{ assignment.course }}</p>
                    <div class="assignment-meta">
                      <span class="meta-date">
                        <i class="bi bi-calendar3 me-1"></i>
                        {{ formatDate(assignment.created_at) }}
                      </span>
                    </div>
                  </div>
                  <div class="assignment-actions">
                    <button class="btn btn-sm btn-outline-primary" @click="editAssignment(assignment.id)">
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-primary" @click="viewSubmissions(assignment.id)">
                      <i class="bi bi-eye"></i>
                    </button>
                  </div>
                </div>
              </div>
              <div v-else class="empty-state-small">
                <i class="bi bi-inbox"></i>
                <p>暂无最近作业</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { user } from '../../stores/auth'
import { teacherAPI } from '../../utils/api'

export default {
  name: 'TeacherDashboard',
  setup() {
    const router = useRouter()
    const stats = ref(null)
    const courses = ref([])
    const assignments = ref([])
    const isLoading = ref(true)
    const error = ref('')

    // 计算属性
    const recentAssignments = computed(() => {
      return assignments.value.slice(0, 3) // 显示最近3个作业
    })

    const pendingSubmissions = computed(() => {
      return assignments.value.filter(a => 
        a.submissions_count > 0 && !a.is_all_graded
      ).length
    })

    const currentDate = computed(() => {
      const now = new Date()
      return now.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      })
    })

    const loadDashboardData = async () => {
      try {
        isLoading.value = true
        error.value = ''
        
        // 获取教师仪表板数据
        const response = await teacherAPI.getDashboard()
        if (response.data.success) {
          const data = response.data.data
          courses.value = data.courses || []
          assignments.value = data.assignments || []
          
        stats.value = {
            coursesCount: data.stats?.courses_count || 0,
            assignmentsCount: data.stats?.assignments_count || 0,
            studentsCount: data.stats?.total_students || 0
          }
        } else {
          throw new Error(response.data.message || '加载失败')
        }
      } catch (err) {
        console.error('加载教师仪表板数据失败:', err)
        error.value = '加载数据失败，请检查网络连接或稍后重试'
        
        // 设置默认值
        courses.value = []
        assignments.value = []
        stats.value = {
          coursesCount: 0,
          assignmentsCount: 0,
          studentsCount: 0
        }
      } finally {
        isLoading.value = false
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    // 导航方法
    const viewCourses = () => {
      router.push('/teacher/courses')
    }

    const viewCourse = (courseId) => {
      router.push(`/teacher/courses/${courseId}`)
    }

    const createAssignment = (courseId = null) => {
      if (courseId) {
        router.push(`/teacher/create-assignment?course=${courseId}`)
      } else {
        router.push('/teacher/create-assignment')
      }
    }

    const editAssignment = (assignmentId) => {
      router.push(`/teacher/assignments/${assignmentId}/edit`)
    }

    const viewSubmissions = (assignmentId) => {
      router.push(`/teacher/assignments/${assignmentId}/submissions`)
    }

    const viewAllAssignments = () => {
      router.push('/teacher/assignments')
    }

    onMounted(() => {
      loadDashboardData()
    })

    return {
      user,
      stats,
      courses,
      assignments,
      recentAssignments,
      pendingSubmissions,
      isLoading,
      error,
      formatDate,
      viewCourses,
      viewCourse,
      createAssignment,
      editAssignment,
      viewSubmissions,
      viewAllAssignments,
      currentDate
    }
  }
}
</script>

<style scoped>
/* 全局样式 */
.teacher-dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 页面头部 */
.page-header {
  margin-bottom: 3rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.header-text h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  margin: 0;
}

.time-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 1rem 1.5rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  color: #475569;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 节标题 */
.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
}

/* 快捷功能区域 */
.quick-actions-section {
  margin-bottom: 3rem;
}

.action-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid #e5e7eb;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.action-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
}

.gradient-warning {
  --gradient-start: #f59e0b;
  --gradient-end: #d97706;
}

.gradient-success {
  --gradient-start: #10b981;
  --gradient-end: #059669;
}

.gradient-info {
  --gradient-start: #3b82f6;
  --gradient-end: #2563eb;
}

.action-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: #d1d5db;
}

.card-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  font-size: 1.75rem;
  color: white;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.card-content h5 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.card-content p {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.btn-custom {
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  font-weight: 600;
  border: none;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.btn-success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.btn-info {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.btn-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

/* 统计卡片 */
.stats-section {
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.stat-primary::before { background: linear-gradient(90deg, #3b82f6, #2563eb); }
.stat-success::before { background: linear-gradient(90deg, #10b981, #059669); }
.stat-info::before { background: linear-gradient(90deg, #06b6d4, #0891b2); }
.stat-warning::before { background: linear-gradient(90deg, #f59e0b, #d97706); }

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
}

.stat-card .stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  margin-bottom: 1rem;
}

.stat-primary .stat-icon { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.stat-success .stat-icon { background: linear-gradient(135deg, #10b981, #059669); }
.stat-info .stat-icon { background: linear-gradient(135deg, #06b6d4, #0891b2); }
.stat-warning .stat-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.stat-trend {
  display: flex;
  align-items: center;
  font-size: 0.75rem;
  color: #9ca3af;
}

.stat-trend i {
  margin-right: 0.25rem;
}

/* 加载状态 */
.loading-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.loading-card {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.loading-text {
  margin-top: 1rem;
  color: #6b7280;
  font-weight: 500;
}

/* 主要内容区域 */
.main-content {
  margin-bottom: 2rem;
}

.content-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header-custom {
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
}

.card-title-custom {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  display: flex;
  align-items: center;
}

.card-body-custom {
  padding: 1.5rem;
}

/* 课程列表 */
.courses-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.course-item {
  background: #f8fafc;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-item:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  transform: translateX(4px);
}

.course-header {
  display: flex;
  align-items: center;
  flex-grow: 1;
}

.course-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
  margin-right: 1rem;
}

.course-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.course-meta {
  display: flex;
  gap: 1rem;
}

.meta-item {
  font-size: 0.875rem;
  color: #6b7280;
  display: flex;
  align-items: center;
}

.course-actions {
  display: flex;
  gap: 0.5rem;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
}

.empty-icon {
  font-size: 4rem;
  color: #d1d5db;
  margin-bottom: 1rem;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.empty-description {
  color: #6b7280;
  margin: 0;
}

.empty-state-small {
  text-align: center;
  padding: 2rem 1rem;
  color: #9ca3af;
}

.empty-state-small i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  display: block;
}

/* 快速操作列表 */
.quick-actions-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.quick-action-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

.quick-action-item:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  transform: translateX(4px);
  color: inherit;
  text-decoration: none;
}

.action-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.125rem;
  margin-right: 0.75rem;
}

.action-text h6 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.125rem;
}

.action-text small {
  font-size: 0.75rem;
  color: #6b7280;
}

.action-arrow {
  margin-left: auto;
  color: #9ca3af;
  font-size: 0.875rem;
}

/* 最近作业 */
.recent-assignments {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.assignment-item {
  background: #f8fafc;
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.assignment-item:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.assignment-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.assignment-course {
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.meta-date {
  font-size: 0.75rem;
  color: #9ca3af;
  display: flex;
  align-items: center;
}

.assignment-actions {
  display: flex;
  gap: 0.5rem;
}

/* 按钮样式 */
.btn {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.btn-outline-primary {
  background: white;
  color: #3b82f6;
  border: 1px solid #3b82f6;
}

.btn-outline-primary:hover {
  background: #3b82f6;
  color: white;
  transform: translateY(-1px);
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .teacher-dashboard {
    padding: 1.5rem 1rem;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .course-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .course-header {
    width: 100%;
  }

  .course-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .assignment-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .assignment-actions {
    align-self: flex-end;
  }

  .action-card {
    padding: 1.5rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-number {
    font-size: 1.5rem;
  }
}

@media (max-width: 576px) {
  .teacher-dashboard {
    padding: 1rem 0.75rem;
  }

  .header-text h1 {
    font-size: 2rem;
  }

  .quick-action-item {
    padding: 0.75rem;
  }

  .action-icon {
    width: 36px;
    height: 36px;
  }
}
</style> 