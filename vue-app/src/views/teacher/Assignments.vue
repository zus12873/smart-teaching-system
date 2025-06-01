<template>
  <div class="teacher-assignments">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1><i class="bi bi-file-earmark-check me-3"></i>作业管理</h1>
          <p class="header-subtitle">管理您的所有作业，跟踪学生提交和评分情况</p>
        </div>
        <div class="header-actions">
          <router-link to="/teacher/create-assignment" class="btn btn-primary btn-lg">
            <i class="bi bi-plus-circle me-2"></i>创建新作业
          </router-link>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section" v-if="!isLoading">
      <div class="row g-4">
        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-primary">
            <div class="stat-icon">
              <i class="bi bi-file-earmark-text"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ assignments.length }}</div>
              <div class="stat-label">全部作业</div>
              <div class="stat-trend">
                <i class="bi bi-arrow-up"></i>
                <span>本学期</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-success">
            <div class="stat-icon">
              <i class="bi bi-check-circle"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ activeAssignments }}</div>
              <div class="stat-label">进行中</div>
              <div class="stat-trend">
                <i class="bi bi-dash"></i>
                <span>活跃状态</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-xl-3 col-md-6">
          <div class="stat-card stat-warning">
            <div class="stat-icon">
              <i class="bi bi-clock"></i>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ expiredAssignments }}</div>
              <div class="stat-label">已过期</div>
              <div class="stat-trend">
                <i class="bi bi-exclamation-triangle"></i>
                <span>需处理</span>
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
              <div class="stat-number">{{ totalSubmissions }}</div>
              <div class="stat-label">总提交数</div>
              <div class="stat-trend">
                <i class="bi bi-arrow-up"></i>
                <span>累计</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 筛选和搜索区域 -->
    <div class="filter-section" v-if="!isLoading">
      <div class="filter-card">
        <div class="filter-header">
          <h3 class="filter-title">
            <i class="bi bi-funnel me-2"></i>筛选作业
          </h3>
          <button class="btn btn-outline-secondary btn-sm" @click="clearFilters">
            <i class="bi bi-arrow-clockwise me-1"></i>重置
          </button>
        </div>
        <div class="filter-body">
          <div class="row g-3">
            <div class="col-md-3">
              <label class="form-label">课程</label>
              <div class="select-wrapper">
                <select v-model="selectedCourse" @change="filterAssignments" class="form-select">
                  <option value="">所有课程</option>
                  <option v-for="course in courses" :key="course.id" :value="course.id">
                    {{ course.name }}
                  </option>
                </select>
                <i class="bi bi-chevron-down select-arrow"></i>
              </div>
            </div>
            <div class="col-md-3">
              <label class="form-label">状态</label>
              <div class="select-wrapper">
                <select v-model="statusFilter" @change="filterAssignments" class="form-select">
                  <option value="">所有状态</option>
                  <option value="active">进行中</option>
                  <option value="expired">已过期</option>
                </select>
                <i class="bi bi-chevron-down select-arrow"></i>
              </div>
            </div>
            <div class="col-md-3">
              <label class="form-label">排序</label>
              <div class="select-wrapper">
                <select v-model="sortBy" @change="filterAssignments" class="form-select">
                  <option value="created_at">创建时间</option>
                  <option value="due_date">截止时间</option>
                  <option value="title">标题</option>
                </select>
                <i class="bi bi-chevron-down select-arrow"></i>
              </div>
            </div>
            <div class="col-md-3">
              <label class="form-label">搜索</label>
              <div class="search-box">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  class="search-input" 
                  placeholder="搜索作业标题..."
                  v-model="searchQuery"
                  @input="filterAssignments"
                >
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
        <p class="loading-text">正在加载作业数据...</p>
      </div>
    </div>

    <!-- 作业列表 -->
    <div class="assignments-section" v-if="!isLoading">
      <div class="section-header">
        <h2 class="section-title">
          <i class="bi bi-grid-3x2-gap me-2"></i>作业列表
          <span class="result-count">({{ filteredAssignments.length }})</span>
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
      <div v-if="viewMode === 'grid'" class="assignments-grid">
        <div v-if="filteredAssignments.length > 0" class="row g-4">
          <div class="col-xl-4 col-lg-6" v-for="assignment in filteredAssignments" :key="assignment.id">
            <div class="assignment-card">
              <div class="assignment-header">
                <div class="assignment-status">
                  <span 
                    class="status-badge"
                    :class="{
                      'status-active': !isExpired(assignment.due_date),
                      'status-expired': isExpired(assignment.due_date)
                    }"
                  >
                    {{ isExpired(assignment.due_date) ? '已过期' : '进行中' }}
                  </span>
                </div>
                <div class="assignment-menu">
                  <div class="dropdown">
                    <button class="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">
                      <i class="bi bi-three-dots"></i>
                    </button>
                    <ul class="dropdown-menu">
                      <li><router-link class="dropdown-item" :to="`/teacher/assignments/${assignment.id}/edit`">
                        <i class="bi bi-pencil me-2"></i>编辑作业
                      </router-link></li>
                      <li><router-link class="dropdown-item" :to="`/teacher/assignments/${assignment.id}/submissions`">
                        <i class="bi bi-eye me-2"></i>查看提交
                      </router-link></li>
                      <li><hr class="dropdown-divider"></li>
                      <li><a class="dropdown-item text-danger" href="#" @click="deleteAssignment(assignment.id)">
                        <i class="bi bi-trash me-2"></i>删除作业
                      </a></li>
                    </ul>
                  </div>
                </div>
              </div>
              
              <div class="assignment-content">
                <div class="assignment-icon">
                  <i class="bi bi-file-earmark-text"></i>
                </div>
                <h3 class="assignment-title">{{ assignment.title }}</h3>
                <p class="assignment-course">{{ assignment.course_name }}</p>
                <p class="assignment-description">{{ assignment.description || '暂无描述' }}</p>
                
                <!-- 作业统计 -->
                <div class="assignment-stats">
                  <div class="stat-row">
                    <div class="stat-item">
                      <i class="bi bi-file-text me-1"></i>
                      <span>{{ assignment.problems_count || 0 }} 题目</span>
                    </div>
                    <div class="stat-item">
                      <i class="bi bi-people me-1"></i>
                      <span>{{ assignment.submissions_count || 0 }} 提交</span>
                    </div>
                  </div>
                  <div class="stat-row">
                    <div class="stat-item">
                      <i class="bi bi-check-circle me-1"></i>
                      <span>{{ assignment.graded_count || 0 }} 已评分</span>
                    </div>
                    <div class="stat-item">
                      <i class="bi bi-clock me-1"></i>
                      <span>{{ formatDate(assignment.created_at) }}</span>
                    </div>
                  </div>
                </div>
                
                <!-- 截止时间 -->
                <div v-if="assignment.due_date" class="due-date-info">
                  <i class="bi bi-calendar-event me-2"></i>
                  <span>截止: {{ formatDateTime(assignment.due_date) }}</span>
                </div>
              </div>
              
              <div class="assignment-actions">
                <router-link 
                  :to="`/teacher/assignments/${assignment.id}/edit`" 
                  class="btn btn-outline-primary btn-sm"
                >
                  <i class="bi bi-pencil me-1"></i>编辑
                </router-link>
                <router-link 
                  :to="`/teacher/assignments/${assignment.id}/submissions`" 
                  class="btn btn-primary btn-sm"
                >
                  <i class="bi bi-eye me-1"></i>查看提交
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="empty-state">
          <div class="empty-icon">
            <i class="bi bi-file-earmark-x"></i>
          </div>
          <h3 class="empty-title">
            {{ searchQuery || selectedCourse || statusFilter ? '未找到匹配的作业' : '暂无作业' }}
          </h3>
          <p class="empty-description">
            {{ searchQuery || selectedCourse || statusFilter ? '请尝试调整筛选条件' : '您还没有创建任何作业，立即开始创建您的第一个作业' }}
          </p>
          <router-link to="/teacher/create-assignment" class="btn btn-primary btn-lg">
            <i class="bi bi-plus-circle me-2"></i>创建作业
          </router-link>
        </div>
      </div>

      <!-- 列表视图 -->
      <div v-if="viewMode === 'list'" class="assignments-list">
        <div v-if="filteredAssignments.length > 0" class="list-container">
          <div class="assignment-list-item" v-for="assignment in filteredAssignments" :key="assignment.id">
            <div class="assignment-list-info">
              <div class="assignment-list-icon">
                <i class="bi bi-file-earmark-text"></i>
              </div>
              <div class="assignment-list-content">
                <div class="assignment-list-header">
                  <h4 class="assignment-list-title">{{ assignment.title }}</h4>
                  <span 
                    class="status-badge"
                    :class="{
                      'status-active': !isExpired(assignment.due_date),
                      'status-expired': isExpired(assignment.due_date)
                    }"
                  >
                    {{ isExpired(assignment.due_date) ? '已过期' : '进行中' }}
                  </span>
                </div>
                <p class="assignment-list-course">{{ assignment.course_name }}</p>
                <p class="assignment-list-description">{{ assignment.description || '暂无描述' }}</p>
                <div class="assignment-list-meta">
                  <span class="meta-item">
                    <i class="bi bi-file-text me-1"></i>
                    {{ assignment.problems_count || 0 }} 题目
                  </span>
                  <span class="meta-item">
                    <i class="bi bi-people me-1"></i>
                    {{ assignment.submissions_count || 0 }} 提交
                  </span>
                  <span class="meta-item">
                    <i class="bi bi-check-circle me-1"></i>
                    {{ assignment.graded_count || 0 }} 已评分
                  </span>
                  <span class="meta-item" v-if="assignment.due_date">
                    <i class="bi bi-calendar-event me-1"></i>
                    截止: {{ formatDateTime(assignment.due_date) }}
                  </span>
                </div>
              </div>
            </div>
            <div class="assignment-list-actions">
              <router-link 
                :to="`/teacher/assignments/${assignment.id}/edit`" 
                class="btn btn-sm btn-outline-primary"
              >
                <i class="bi bi-pencil me-1"></i>编辑
              </router-link>
              <router-link 
                :to="`/teacher/assignments/${assignment.id}/submissions`" 
                class="btn btn-sm btn-primary"
              >
                <i class="bi bi-eye me-1"></i>查看提交
              </router-link>
              <button 
                class="btn btn-sm btn-outline-danger"
                @click="deleteAssignment(assignment.id)"
              >
                <i class="bi bi-trash me-1"></i>删除
              </button>
            </div>
          </div>
        </div>

        <!-- 列表空状态 -->
        <div v-else class="empty-state">
          <div class="empty-icon">
            <i class="bi bi-search"></i>
          </div>
          <h3 class="empty-title">未找到匹配的作业</h3>
          <p class="empty-description">请尝试调整筛选条件或搜索关键词</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { teacherAPI } from '../../utils/api'

export default {
  name: 'TeacherAssignments',
  setup() {
    const router = useRouter()
    
    const isLoading = ref(true)
    const assignments = ref([])
    const courses = ref([])
    
    const selectedCourse = ref('')
    const statusFilter = ref('')
    const searchQuery = ref('')
    const sortBy = ref('created_at')
    const viewMode = ref('grid')

    // 计算统计数据
    const activeAssignments = computed(() => {
      return assignments.value.filter(a => !isExpired(a.due_date)).length
    })

    const expiredAssignments = computed(() => {
      return assignments.value.filter(a => isExpired(a.due_date)).length
    })

    const totalSubmissions = computed(() => {
      return assignments.value.reduce((total, a) => total + (a.submissions_count || 0), 0)
    })

    const loadData = async () => {
      isLoading.value = true
      try {
        // 并行加载作业和课程数据
        const [assignmentsResponse, coursesResponse] = await Promise.all([
          teacherAPI.getAssignments(),
          teacherAPI.getCourses()
        ])
        
        if (assignmentsResponse.data.success) {
          assignments.value = assignmentsResponse.data.assignments || []
        }
        
        if (coursesResponse.data.success) {
          courses.value = coursesResponse.data.courses || []
        }
      } catch (error) {
        console.error('加载数据失败:', error)
        alert('加载数据失败')
      } finally {
        isLoading.value = false
      }
    }

    const filteredAssignments = computed(() => {
      let filtered = [...assignments.value]
      
      // 按课程筛选
      if (selectedCourse.value) {
        filtered = filtered.filter(a => a.course_id == selectedCourse.value)
      }
      
      // 按状态筛选
      if (statusFilter.value) {
        if (statusFilter.value === 'active') {
          filtered = filtered.filter(a => !isExpired(a.due_date))
        } else if (statusFilter.value === 'expired') {
          filtered = filtered.filter(a => isExpired(a.due_date))
        }
      }
      
      // 搜索筛选
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(a => 
          a.title.toLowerCase().includes(query) ||
          (a.description && a.description.toLowerCase().includes(query))
        )
      }
      
      // 排序
      filtered.sort((a, b) => {
        switch (sortBy.value) {
          case 'title':
            return a.title.localeCompare(b.title)
          case 'due_date':
            if (!a.due_date && !b.due_date) return 0
            if (!a.due_date) return 1
            if (!b.due_date) return -1
            return new Date(a.due_date) - new Date(b.due_date)
          case 'created_at':
          default:
            return new Date(b.created_at) - new Date(a.created_at)
        }
      })
      
      return filtered
    })

    const filterAssignments = () => {
      // 过滤函数，由computed属性自动处理
    }

    const isExpired = (dueDate) => {
      if (!dueDate) return false
      return new Date(dueDate) < new Date()
    }

    const formatDateTime = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    const deleteAssignment = async (assignmentId) => {
      if (!confirm('确定要删除这个作业吗？此操作无法撤销。')) {
        return
      }
      
      try {
        const response = await teacherAPI.deleteAssignment(assignmentId)
        if (response.data.success) {
          assignments.value = assignments.value.filter(a => a.id !== assignmentId)
          alert('作业删除成功')
        } else {
          throw new Error(response.data.message || '删除失败')
        }
      } catch (error) {
        console.error('删除作业失败:', error)
        alert('删除作业失败: ' + error.message)
      }
    }

    const clearFilters = () => {
      selectedCourse.value = ''
      statusFilter.value = ''
      searchQuery.value = ''
      sortBy.value = 'created_at'
    }

    onMounted(() => {
      loadData()
    })

    return {
      isLoading,
      assignments,
      courses,
      selectedCourse,
      statusFilter,
      searchQuery,
      sortBy,
      viewMode,
      activeAssignments,
      expiredAssignments,
      totalSubmissions,
      filteredAssignments,
      filterAssignments,
      isExpired,
      formatDateTime,
      formatDate,
      deleteAssignment,
      clearFilters
    }
  }
}
</script>

<style scoped>
/* 全局样式 */
.teacher-assignments {
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

.header-actions .btn-lg {
  padding: 0.875rem 2rem;
  font-size: 1rem;
  border-radius: 12px;
  font-weight: 600;
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

/* 筛选区域 */
.filter-section {
  margin-bottom: 3rem;
}

.filter-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
}

.filter-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  display: flex;
  align-items: center;
}

.filter-body {
  padding: 1.5rem;
}

.form-label {
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.select-wrapper {
  position: relative;
}

.form-select {
  appearance: none;
  padding: 0.75rem 3rem 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  background: white;
  width: 100%;
}

.form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.select-arrow {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
}

.search-box {
  position: relative;
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
  border-radius: 8px;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  background: white;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
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

/* 作业列表区域 */
.assignments-section {
  margin-bottom: 2rem;
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

.result-count {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 400;
  margin-left: 0.5rem;
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
.assignments-grid {
  margin-bottom: 2rem;
}

.assignment-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
}

.assignment-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: #d1d5db;
}

.assignment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem 1.5rem 0;
}

.assignment-status {
  flex-grow: 1;
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

.status-expired {
  background: #fecaca;
  color: #dc2626;
}

.assignment-menu {
  margin-left: 1rem;
}

.assignment-content {
  padding: 1rem 1.5rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.assignment-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.assignment-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
  line-height: 1.3;
}

.assignment-course {
  font-size: 0.875rem;
  color: #3b82f6;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.assignment-description {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  flex-grow: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.assignment-stats {
  margin-bottom: 1rem;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.stat-row:last-child {
  margin-bottom: 0;
}

.stat-item {
  display: flex;
  align-items: center;
  font-size: 0.75rem;
  color: #6b7280;
  flex: 1;
}

.due-date-info {
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
  font-size: 0.75rem;
  color: #374151;
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.assignment-actions {
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border-top: 1px solid #f3f4f6;
  display: flex;
  gap: 0.5rem;
}

/* 列表视图 */
.assignments-list {
  margin-bottom: 2rem;
}

.list-container {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.assignment-list-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem;
  border-bottom: 1px solid #f3f4f6;
  transition: all 0.2s ease;
}

.assignment-list-item:last-child {
  border-bottom: none;
}

.assignment-list-item:hover {
  background: #f8fafc;
}

.assignment-list-info {
  display: flex;
  align-items: flex-start;
  flex-grow: 1;
}

.assignment-list-icon {
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

.assignment-list-content {
  flex-grow: 1;
}

.assignment-list-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.assignment-list-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  flex-grow: 1;
  margin-right: 1rem;
}

.assignment-list-course {
  font-size: 0.875rem;
  color: #3b82f6;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.assignment-list-description {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.assignment-list-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  font-size: 0.75rem;
  color: #9ca3af;
}

.assignment-list-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
  margin-left: 1rem;
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
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
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
  text-decoration: none;
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

.btn-outline-danger {
  background: white;
  color: #dc2626;
  border: 1px solid #dc2626;
}

.btn-outline-danger:hover {
  background: #dc2626;
  color: white;
  transform: translateY(-1px);
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
  text-decoration: none;
}

.dropdown-item:hover {
  background: #f3f4f6;
  color: #1f2937;
  text-decoration: none;
}

.dropdown-item.text-danger {
  color: #dc2626;
}

.dropdown-item.text-danger:hover {
  background: #fef2f2;
  color: #dc2626;
}

.dropdown-divider {
  margin: 0.5rem 0;
  border-color: #e5e7eb;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .teacher-assignments {
    padding: 1.5rem 1rem;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .assignment-list-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .assignment-list-info {
    width: 100%;
  }

  .assignment-list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .assignment-list-actions {
    width: 100%;
    justify-content: flex-end;
    margin-left: 0;
  }

  .filter-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .assignment-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .assignment-actions .btn {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .teacher-assignments {
    padding: 1rem 0.75rem;
  }

  .header-text h1 {
    font-size: 2rem;
  }

  .stats-section .row {
    margin: 0 -0.5rem;
  }

  .stats-section .col-xl-3 {
    padding: 0 0.5rem;
    margin-bottom: 1rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-number {
    font-size: 1.5rem;
  }

  .assignment-list-meta {
    flex-direction: column;
    gap: 0.5rem;
  }

  .assignment-list-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .assignment-list-actions .btn {
    width: 100%;
  }
}
</style> 