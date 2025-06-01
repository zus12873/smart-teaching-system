<template>
  <div class="teacher-courses">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1><i class="bi bi-journal-bookmark me-3"></i>我的课程</h1>
          <p class="header-subtitle">管理您的教学课程和教学资源</p>
        </div>
        <div class="header-actions">
          <div class="search-box">
            <i class="bi bi-search search-icon"></i>
            <input 
              type="text" 
              class="search-input" 
              placeholder="搜索课程..." 
              v-model="searchQuery"
              @input="filterCourses"
            >
          </div>
        </div>
      </div>
    </div>

    <!-- 课程统计卡片 -->
    <div class="stats-section" v-if="!isLoading">
      <div class="row g-4">
        <div class="col-md-3">
          <div class="stat-card stat-primary">
            <div class="stat-icon">
              <i class="bi bi-journal-album"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ filteredCourses.length }}</div>
              <div class="stat-label">我的课程</div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card stat-success">
            <div class="stat-icon">
              <i class="bi bi-people"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ totalStudents }}</div>
              <div class="stat-label">总学生数</div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card stat-info">
            <div class="stat-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ totalAssignments }}</div>
              <div class="stat-label">总作业数</div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card stat-warning">
            <div class="stat-icon">
              <i class="bi bi-clock-history"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ activeCourses }}</div>
              <div class="stat-label">活跃课程</div>
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
        <p class="loading-text">正在加载课程信息...</p>
      </div>
    </div>

    <!-- 课程列表 -->
    <div class="courses-section" v-if="!isLoading">
      <div class="section-header">
        <h2 class="section-title">
          <i class="bi bi-grid-3x2-gap me-2"></i>课程列表
        </h2>
        <div class="view-options">
          <div class="btn-group" role="group">
            <button 
              class="btn btn-outline-secondary btn-sm" 
              :class="{ active: viewMode === 'grid' }"
              @click="viewMode = 'grid'"
            >
              <i class="bi bi-grid-3x2-gap"></i>
            </button>
            <button 
              class="btn btn-outline-secondary btn-sm" 
              :class="{ active: viewMode === 'list' }"
              @click="viewMode = 'list'"
            >
              <i class="bi bi-list"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- 网格视图 -->
      <div v-if="viewMode === 'grid'" class="courses-grid">
        <div v-if="filteredCourses.length > 0" class="row g-4">
          <div class="col-xl-4 col-lg-6 col-md-6" v-for="course in filteredCourses" :key="course.id">
            <div class="course-card">
              <div class="course-header">
                <div class="course-icon">
                  <i class="bi bi-book"></i>
                </div>
                <div class="course-status">
                  <span class="status-badge status-active">活跃</span>
                </div>
              </div>
              <div class="course-content">
                <h3 class="course-title">{{ course.name }}</h3>
                <p class="course-description">{{ course.description || '暂无课程描述' }}</p>
                
                <div class="course-stats">
                  <div class="stat-item">
                    <i class="bi bi-people me-2"></i>
                    <span>{{ course.studentsCount || 0 }} 名学生</span>
                  </div>
                  <div class="stat-item">
                    <i class="bi bi-file-text me-2"></i>
                    <span>{{ course.assignmentsCount || 0 }} 个作业</span>
                  </div>
                </div>

                <div class="course-meta">
                  <span class="meta-date">
                    <i class="bi bi-calendar3 me-1"></i>
                    创建于 {{ formatDate(course.created_at) }}
                  </span>
                </div>
              </div>
              <div class="course-actions">
                <button 
                  class="btn btn-primary btn-sm"
                  @click="viewCourseDetail(course.id)"
                >
                  <i class="bi bi-eye me-1"></i>查看详情
                </button>
                <div class="dropdown">
                  <button class="btn btn-outline-secondary btn-sm dropdown-toggle" data-bs-toggle="dropdown">
                    <i class="bi bi-three-dots"></i>
                  </button>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#" @click="createAssignment(course.id)">
                      <i class="bi bi-plus-circle me-2"></i>布置作业
                    </a></li>
                    <li><a class="dropdown-item" href="#" @click="viewStudents(course.id)">
                      <i class="bi bi-people me-2"></i>查看学生
                    </a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" @click="exportCourseData(course.id)">
                      <i class="bi bi-download me-2"></i>导出数据
                    </a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="empty-state">
          <div class="empty-icon">
            <i class="bi bi-journal-x"></i>
          </div>
          <h3 class="empty-title">暂无课程</h3>
          <p class="empty-description">您目前没有负责的课程，请联系管理员为您分配课程</p>
          <button class="btn btn-primary" @click="contactAdmin">
            <i class="bi bi-envelope me-2"></i>联系管理员
          </button>
        </div>
      </div>

      <!-- 列表视图 -->
      <div v-if="viewMode === 'list'" class="courses-list">
        <div v-if="filteredCourses.length > 0" class="list-container">
          <div class="course-list-item" v-for="course in filteredCourses" :key="course.id">
            <div class="course-list-info">
              <div class="course-list-icon">
                <i class="bi bi-journal-bookmark"></i>
              </div>
              <div class="course-list-content">
                <h4 class="course-list-title">{{ course.name }}</h4>
                <p class="course-list-description">{{ course.description || '暂无课程描述' }}</p>
                <div class="course-list-meta">
                  <span class="meta-item">
                    <i class="bi bi-calendar3 me-1"></i>
                    {{ formatDate(course.created_at) }}
                  </span>
                  <span class="meta-item">
                    <i class="bi bi-people me-1"></i>
                    {{ course.studentsCount || 0 }} 名学生
                  </span>
                  <span class="meta-item">
                    <i class="bi bi-file-text me-1"></i>
                    {{ course.assignmentsCount || 0 }} 个作业
                  </span>
                </div>
              </div>
            </div>
            <div class="course-list-actions">
              <button class="btn btn-sm btn-outline-primary" @click="viewCourseDetail(course.id)">
                <i class="bi bi-eye me-1"></i>查看
              </button>
              <button class="btn btn-sm btn-primary" @click="createAssignment(course.id)">
                <i class="bi bi-plus me-1"></i>布置作业
              </button>
            </div>
          </div>
        </div>

        <!-- 列表空状态 -->
        <div v-else class="empty-state">
          <div class="empty-icon">
            <i class="bi bi-search"></i>
          </div>
          <h3 class="empty-title">未找到匹配的课程</h3>
          <p class="empty-description">请尝试其他搜索关键词</p>
        </div>
      </div>
    </div>

    <!-- 智能教学资源区域 -->
    <div class="resources-section" v-if="!isLoading">
      <h2 class="section-title">
        <i class="bi bi-magic me-2"></i>智能教学工具
      </h2>
      <div class="row g-4">
        <div class="col-lg-4 col-md-6">
          <div class="resource-card resource-primary">
            <div class="resource-icon">
              <i class="bi bi-plus-circle"></i>
            </div>
            <div class="resource-content">
              <h4>创建作业</h4>
              <p>为您的课程创建新的作业，支持多种题型和智能评分</p>
              <button class="btn btn-primary" @click="createAssignment">
                <i class="bi bi-arrow-right me-2"></i>开始创建
              </button>
            </div>
          </div>
        </div>
        
        <div class="col-lg-4 col-md-6">
          <div class="resource-card resource-warning">
            <div class="resource-icon">
              <i class="bi bi-lightbulb"></i>
            </div>
            <div class="resource-content">
              <h4>智能出题</h4>
              <p>使用AI技术自动生成高质量试题，节省出题时间</p>
              <router-link to="/problem-generation" class="btn btn-warning">
                <i class="bi bi-arrow-right me-2"></i>立即体验
              </router-link>
            </div>
          </div>
        </div>
        
        <div class="col-lg-4 col-md-6">
          <div class="resource-card resource-success">
            <div class="resource-icon">
              <i class="bi bi-robot"></i>
            </div>
            <div class="resource-content">
              <h4>智能批改</h4>
              <p>自动批改学生作业，提供详细的评分和反馈</p>
              <router-link to="/multi-upload" class="btn btn-success">
                <i class="bi bi-arrow-right me-2"></i>开始批改
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { teacherAPI } from '../../utils/api'

export default {
  name: 'TeacherCourses',
  setup() {
    const router = useRouter()
    const courses = ref([])
    const isLoading = ref(true)
    const searchQuery = ref('')
    const viewMode = ref('grid')

    const filteredCourses = computed(() => {
      if (!searchQuery.value) return courses.value
      return courses.value.filter(course => 
        course.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        (course.description && course.description.toLowerCase().includes(searchQuery.value.toLowerCase()))
      )
    })

    const loadCourses = async () => {
      try {
        const response = await teacherAPI.getCourses()
        if (response.data.success) {
          courses.value = response.data.courses.map(course => ({
            ...course,
            studentsCount: course.students_count || 0,
            assignmentsCount: course.assignments_count || 0
          }))
        } else {
          throw new Error(response.data.message || '加载课程失败')
        }
      } catch (error) {
        console.error('加载课程失败:', error)
        // 可以在这里显示错误提示
      } finally {
        isLoading.value = false
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    const viewCourseDetail = (courseId) => {
      router.push(`/teacher/courses/${courseId}`)
    }

    const createAssignment = (courseId) => {
      router.push(`/teacher/create-assignment?courseId=${courseId}`)
    }

    const filterCourses = () => {
      // 搜索功能已通过computed属性实现
    }

    const totalStudents = computed(() => {
      return courses.value.reduce((total, course) => total + course.studentsCount, 0)
    })

    const totalAssignments = computed(() => {
      return courses.value.reduce((total, course) => total + course.assignmentsCount, 0)
    })

    const activeCourses = computed(() => {
      return courses.value.filter(course => course.status === 'active').length
    })

    const viewStudents = (courseId) => {
      router.push(`/teacher/students?courseId=${courseId}`)
    }

    const exportCourseData = (courseId) => {
      // 实现导出课程数据的功能
    }

    const contactAdmin = () => {
      // 实现联系管理员的功能
    }

    onMounted(() => {
      loadCourses()
    })

    return {
      courses,
      filteredCourses,
      isLoading,
      searchQuery,
      viewMode,
      formatDate,
      viewCourseDetail,
      createAssignment,
      filterCourses,
      totalStudents,
      totalAssignments,
      activeCourses,
      viewStudents,
      exportCourseData,
      contactAdmin
    }
  }
}
</script>

<style scoped>
/* 全局样式 */
.teacher-courses {
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

.search-box {
  position: relative;
  width: 320px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  font-size: 1rem;
  z-index: 10;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  background: white;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
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
}

/* 加载状态 */
.loading-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.loading-card {
  text-align: center;
  padding: 3rem;
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

/* 课程列表区域 */
.courses-section {
  margin-bottom: 3rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  display: flex;
  align-items: center;
  margin: 0;
}

.view-options .btn-group {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.view-options .btn {
  border: none;
  padding: 0.5rem 0.75rem;
  background: white;
  color: #6b7280;
  transition: all 0.2s ease;
}

.view-options .btn.active {
  background: #3b82f6;
  color: white;
}

.view-options .btn:hover:not(.active) {
  background: #f3f4f6;
  color: #374151;
}

/* 网格视图 */
.courses-grid {
  margin-bottom: 2rem;
}

.course-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
  overflow: hidden;
  position: relative;
}

.course-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: #d1d5db;
}

.course-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem 1.5rem 0;
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
}

.course-status {
  margin-left: auto;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-active {
  background: #d1fae5;
  color: #047857;
}

.course-content {
  padding: 1rem 1.5rem;
  flex-grow: 1;
}

.course-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.course-description {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #6b7280;
}

.course-meta {
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

.meta-date {
  font-size: 0.75rem;
  color: #9ca3af;
  display: flex;
  align-items: center;
}

.course-actions {
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border-top: 1px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 列表视图 */
.courses-list {
  margin-bottom: 2rem;
}

.list-container {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.course-list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #f3f4f6;
  transition: all 0.2s ease;
}

.course-list-item:last-child {
  border-bottom: none;
}

.course-list-item:hover {
  background: #f8fafc;
}

.course-list-info {
  display: flex;
  align-items: flex-start;
  flex-grow: 1;
}

.course-list-icon {
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
  flex-shrink: 0;
}

.course-list-content {
  flex-grow: 1;
}

.course-list-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.course-list-description {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.course-list-meta {
  display: flex;
  gap: 1.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  font-size: 0.75rem;
  color: #9ca3af;
}

.course-list-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
}

.empty-icon {
  font-size: 4rem;
  color: #d1d5db;
  margin-bottom: 1.5rem;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.empty-description {
  color: #6b7280;
  margin-bottom: 2rem;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

/* 智能教学资源区域 */
.resources-section {
  margin-bottom: 2rem;
}

.resource-card {
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

.resource-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.resource-primary::before { background: linear-gradient(90deg, #3b82f6, #2563eb); }
.resource-warning::before { background: linear-gradient(90deg, #f59e0b, #d97706); }
.resource-success::before { background: linear-gradient(90deg, #10b981, #059669); }

.resource-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: #d1d5db;
}

.resource-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  font-size: 1.75rem;
  color: white;
}

.resource-primary .resource-icon { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.resource-warning .resource-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }
.resource-success .resource-icon { background: linear-gradient(135deg, #10b981, #059669); }

.resource-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.resource-content h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.resource-content p {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  flex-grow: 1;
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
  text-decoration: none;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  padding: 0.75rem 1.5rem;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
  color: white;
  text-decoration: none;
}

.btn-warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  padding: 0.75rem 1.5rem;
}

.btn-warning:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(245, 158, 11, 0.3);
  color: white;
  text-decoration: none;
}

.btn-success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 0.75rem 1.5rem;
}

.btn-success:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
  color: white;
  text-decoration: none;
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

.btn-outline-secondary {
  background: white;
  color: #6b7280;
  border: 1px solid #d1d5db;
}

.btn-outline-secondary:hover {
  background: #f3f4f6;
  color: #374151;
  border-color: #9ca3af;
}

/* 下拉菜单 */
.dropdown-menu {
  border: none;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  padding: 0.5rem 0;
}

.dropdown-item {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  color: #374151;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.dropdown-divider {
  margin: 0.5rem 0;
  border-color: #e5e7eb;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .teacher-courses {
    padding: 1.5rem 1rem;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }

  .search-box {
    width: 100%;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .course-list-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .course-list-info {
    width: 100%;
  }

  .course-list-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .resource-card {
    padding: 1.5rem;
  }
}

@media (max-width: 576px) {
  .teacher-courses {
    padding: 1rem 0.75rem;
  }

  .header-text h1 {
    font-size: 2rem;
  }

  .stats-section .row {
    margin: 0 -0.5rem;
  }

  .stats-section .col-md-3 {
    padding: 0 0.5rem;
    margin-bottom: 1rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-number {
    font-size: 1.5rem;
  }

  .course-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .course-actions .btn {
    width: 100%;
  }
}
</style>
