<template>
  <div class="view-submissions-page">
    <!-- 顶部导航栏 -->
    <div class="top-navigation">
      <div class="nav-content">
        <div class="nav-left">
          <router-link to="/teacher/assignments" class="back-button">
            <i class="bi bi-arrow-left"></i>
            <span>返回作业列表</span>
          </router-link>
          <div class="breadcrumb">
            <span class="breadcrumb-item">{{ assignment?.course_name || '课程' }}</span>
            <i class="bi bi-chevron-right"></i>
            <span class="breadcrumb-current">{{ assignment?.title || '作业' }} - 查看提交</span>
          </div>
        </div>
        <div class="nav-right">
          <button class="refresh-button" @click="loadSubmissions" :disabled="isLoading">
            <i class="bi bi-arrow-clockwise" :class="{ 'spin': isLoading }"></i>
            <span>刷新</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content" v-if="!isLoading">
      <!-- 统计信息卡片 -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon student-icon">
            <i class="bi bi-people-fill"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ statistics?.total_students || 0 }}</div>
            <div class="stat-label">总学生数</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon submitted-icon">
            <i class="bi bi-check-circle-fill"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ statistics?.submitted_count || 0 }}</div>
            <div class="stat-label">已提交</div>
            <div class="stat-percent">{{ statistics?.submission_rate || 0 }}%</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon pending-icon">
            <i class="bi bi-clock-fill"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ statistics?.unsubmitted_count || 0 }}</div>
            <div class="stat-label">未提交</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon graded-icon">
            <i class="bi bi-clipboard-check-fill"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ statistics?.graded_count || 0 }}</div>
            <div class="stat-label">已评分</div>
            <div class="stat-percent" v-if="statistics?.average_score !== null">
              平均分: {{ statistics?.average_score || 0 }}
            </div>
          </div>
        </div>
      </div>

      <!-- 筛选和搜索 -->
      <div class="filter-section">
        <div class="filter-left">
          <div class="filter-group">
            <label>状态筛选:</label>
            <select v-model="statusFilter" @change="filterSubmissions" class="filter-select">
              <option value="all">全部</option>
              <option value="submitted">已提交</option>
              <option value="unsubmitted">未提交</option>
              <option value="graded">已评分</option>
              <option value="ungraded">未评分</option>
            </select>
          </div>
        </div>
        <div class="filter-right">
          <div class="search-box">
            <i class="bi bi-search"></i>
            <input 
              type="text" 
              v-model="searchQuery" 
              @input="filterSubmissions"
              placeholder="搜索学生姓名..."
              class="search-input"
            >
          </div>
        </div>
      </div>

      <!-- 提交列表 -->
      <div class="submissions-container">
        <div class="submissions-header">
          <h2><i class="bi bi-list-ul"></i>学生提交情况</h2>
          <div class="header-actions">
            <button class="export-button" @click="exportSubmissions">
              <i class="bi bi-download"></i>
              导出Excel
            </button>
          </div>
        </div>

        <div class="submissions-table">
          <table>
            <thead>
              <tr>
                <th>学生</th>
                <th>邮箱</th>
                <th>提交状态</th>
                <th>提交时间</th>
                <th>答题进度</th>
                <th>评分状态</th>
                <th>总分</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="submission in filteredSubmissions" :key="submission.student_id" class="submission-row">
                <td>
                  <div class="student-info">
                    <div class="student-avatar">
                      {{ submission.student_name?.charAt(0) || 'S' }}
                    </div>
                    <span class="student-name">{{ submission.student_name }}</span>
                  </div>
                </td>
                <td>{{ submission.student_email }}</td>
                <td>
                  <span 
                    class="status-badge" 
                    :class="{
                      'status-submitted': submission.status === '已提交',
                      'status-unsubmitted': submission.status === '未提交'
                    }"
                  >
                    {{ submission.status }}
                  </span>
                </td>
                <td>
                  <span v-if="submission.submitted_at" class="submit-time">
                    {{ formatDateTime(submission.submitted_at) }}
                  </span>
                  <span v-else class="no-submit">-</span>
                </td>
                <td>
                  <div class="progress-info">
                    <div class="progress-bar">
                      <div 
                        class="progress-fill" 
                        :style="{ width: getProgressPercentage(submission) + '%' }"
                      ></div>
                    </div>
                    <span class="progress-text">
                      {{ submission.answered_count }} / {{ submission.problem_count }}
                    </span>
                  </div>
                </td>
                <td>
                  <span 
                    class="grade-badge"
                    :class="{
                      'grade-graded': submission.is_graded,
                      'grade-ungraded': !submission.is_graded && submission.status === '已提交',
                      'grade-na': submission.status === '未提交'
                    }"
                  >
                    {{ getGradeStatus(submission) }}
                  </span>
                </td>
                <td>
                  <span v-if="submission.total_score !== null" class="score">
                    {{ Math.round(submission.total_score * 10) / 10 }}分
                  </span>
                  <span v-else class="no-score">-</span>
                </td>
                <td>
                  <div class="actions">
                    <button 
                      v-if="submission.status === '已提交'" 
                      class="view-button" 
                      @click="viewSubmissionDetail(submission)"
                      title="查看详情"
                    >
                      <i class="bi bi-eye"></i>
                    </button>
                    <button 
                      v-if="submission.status === '已提交' && !submission.is_graded" 
                      class="grade-button" 
                      @click="gradeSubmission(submission)"
                      title="评分"
                    >
                      <i class="bi bi-pencil-square"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          
          <div v-if="filteredSubmissions.length === 0" class="empty-state">
            <i class="bi bi-inbox"></i>
            <p>没有找到符合条件的提交记录</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>正在加载提交信息...</p>
    </div>

    <!-- 提交详情模态框 -->
    <div v-if="selectedSubmission" class="modal-overlay" @click="closeDetail">
      <div class="detail-modal" @click.stop>
        <div class="modal-header">
          <h3>
            <i class="bi bi-file-text"></i>
            {{ selectedSubmission.student_name }} 的作业提交
          </h3>
          <button class="close-button" @click="closeDetail">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="submission-meta">
            <div class="meta-item">
              <strong>提交时间:</strong> {{ formatDateTime(selectedSubmission.submitted_at) }}
            </div>
            <div class="meta-item">
              <strong>总分:</strong> 
              <span v-if="selectedSubmission.total_score !== null">
                {{ Math.round(selectedSubmission.total_score * 10) / 10 }}分
              </span>
              <span v-else>未评分</span>
            </div>
            <div class="meta-item">
              <strong>评分状态:</strong> 
              <span :class="{ 'graded': selectedSubmission.is_graded, 'ungraded': !selectedSubmission.is_graded }">
                {{ selectedSubmission.is_graded ? '已评分' : '待评分' }}
              </span>
            </div>
          </div>

          <div class="problems-section">
            <h4>题目答案详情</h4>
            <div v-for="problem in selectedSubmission.problems" :key="problem.problem_id" class="problem-detail">
              <div class="problem-header">
                <span class="problem-number">第 {{ problem.order }} 题</span>
                <span v-if="problem.score !== null" class="problem-score">
                  得分: {{ Math.round(problem.score * 10) / 10 }}分
                </span>
              </div>
              
              <div class="problem-content">
                <div class="problem-text">
                  <strong>题目:</strong>
                  <div v-html="renderMarkdown(problem.problem_text)"></div>
                </div>
                
                <div v-if="problem.answer" class="student-answer">
                  <strong>学生答案:</strong>
                  <div class="answer-content" v-html="renderMarkdown(problem.answer)"></div>
                </div>
                <div v-else class="no-answer">
                  <em>未作答</em>
                </div>
                
                <div v-if="problem.grading_result" class="grading-result">
                  <strong>评分结果:</strong>
                  <div class="result-content" v-html="renderMarkdown(problem.grading_result)"></div>
                </div>
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
import { useRoute, useRouter } from 'vue-router'
import { teacherAPI } from '../../utils/api'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js/lib/core'
import javascript from 'highlight.js/lib/languages/javascript'
import python from 'highlight.js/lib/languages/python'
import java from 'highlight.js/lib/languages/java'
import cpp from 'highlight.js/lib/languages/cpp'
import sql from 'highlight.js/lib/languages/sql'
import xml from 'highlight.js/lib/languages/xml'
import 'highlight.js/styles/github.css'

// 注册常用编程语言
hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('python', python)
hljs.registerLanguage('java', java)
hljs.registerLanguage('cpp', cpp)
hljs.registerLanguage('sql', sql)
hljs.registerLanguage('html', xml)
hljs.registerLanguage('xml', xml)

// 配置markdown-it
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (__) {}
    }
    return ''
  }
})

export default {
  name: 'ViewSubmissions',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const assignmentId = route.params.id
    
    const isLoading = ref(true)
    const assignment = ref(null)
    const submissions = ref([])
    const statistics = ref(null)
    const problems = ref([])
    
    const statusFilter = ref('all')
    const searchQuery = ref('')
    const selectedSubmission = ref(null)

    const loadSubmissions = async () => {
      isLoading.value = true
      try {
        const response = await teacherAPI.getSubmissions(assignmentId)
        if (response.data.success) {
          assignment.value = response.data.data.assignment
          submissions.value = response.data.data.submissions
          statistics.value = response.data.data.statistics
          problems.value = response.data.data.problems
        } else {
          throw new Error(response.data.message || '加载失败')
        }
      } catch (error) {
        console.error('加载提交信息失败:', error)
        alert('加载提交信息失败')
        router.push('/teacher/assignments')
      } finally {
        isLoading.value = false
      }
    }

    const filteredSubmissions = computed(() => {
      let filtered = [...submissions.value]
      
      // 状态筛选
      if (statusFilter.value !== 'all') {
        filtered = filtered.filter(sub => {
          switch (statusFilter.value) {
            case 'submitted':
              return sub.status === '已提交'
            case 'unsubmitted':
              return sub.status === '未提交'
            case 'graded':
              return sub.is_graded
            case 'ungraded':
              return sub.status === '已提交' && !sub.is_graded
            default:
              return true
          }
        })
      }
      
      // 搜索筛选
      if (searchQuery.value.trim()) {
        const query = searchQuery.value.toLowerCase().trim()
        filtered = filtered.filter(sub => 
          sub.student_name.toLowerCase().includes(query) ||
          sub.student_email.toLowerCase().includes(query)
        )
      }
      
      return filtered
    })

    const filterSubmissions = () => {
      // 筛选逻辑已在computed中处理
    }

    const getProgressPercentage = (submission) => {
      if (submission.problem_count === 0) return 0
      return Math.round((submission.answered_count / submission.problem_count) * 100)
    }

    const getGradeStatus = (submission) => {
      if (submission.status === '未提交') return '未提交'
      if (submission.is_graded) return '已评分'
      return '待评分'
    }

    const formatDateTime = (dateTimeString) => {
      if (!dateTimeString) return '-'
      const date = new Date(dateTimeString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const viewSubmissionDetail = (submission) => {
      selectedSubmission.value = submission
    }

    const closeDetail = () => {
      selectedSubmission.value = null
    }

    const gradeSubmission = (submission) => {
      // TODO: 实现评分功能
      alert('评分功能待实现')
    }

    const exportSubmissions = () => {
      // TODO: 实现导出Excel功能
      alert('导出功能待实现')
    }

    const renderMarkdown = (text) => {
      if (!text) return ''
      
      try {
        let html = md.render(text)
        html = html.replace(/<a href="http/g, '<a target="_blank" rel="noopener noreferrer" href="http')
        return html
      } catch (error) {
        console.error('Markdown渲染错误:', error)
        return text.replace(/\n/g, '<br>')
      }
    }

    onMounted(() => {
      loadSubmissions()
    })

    return {
      isLoading,
      assignment,
      submissions,
      statistics,
      problems,
      statusFilter,
      searchQuery,
      selectedSubmission,
      filteredSubmissions,
      loadSubmissions,
      filterSubmissions,
      getProgressPercentage,
      getGradeStatus,
      formatDateTime,
      viewSubmissionDetail,
      closeDetail,
      gradeSubmission,
      exportSubmissions,
      renderMarkdown
    }
  }
}
</script>

<style scoped>
.view-submissions-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 顶部导航栏 */
.top-navigation {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #e2e8f0;
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #475569;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
  padding: 0.5rem 1rem;
  border-radius: 8px;
}

.back-button:hover {
  background: rgba(71, 85, 105, 0.1);
  color: #334155;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.875rem;
}

.breadcrumb-current {
  color: #1e293b;
  font-weight: 500;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #475569;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
  cursor: pointer;
}

.refresh-button:hover:not(:disabled) {
  background: #334155;
}

.refresh-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 主要内容区域 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* 统计信息卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.student-icon { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
.submitted-icon { background: linear-gradient(135deg, #10b981, #059669); }
.pending-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }
.graded-icon { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
}

.stat-label {
  color: #64748b;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.stat-percent {
  color: #059669;
  font-size: 0.75rem;
  font-weight: 500;
  margin-top: 0.25rem;
}

/* 筛选区域 */
.filter-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

.filter-select {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  min-width: 120px;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box i {
  position: absolute;
  left: 0.75rem;
  color: #9ca3af;
  z-index: 1;
}

.search-input {
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  min-width: 250px;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* 提交列表容器 */
.submissions-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.submissions-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.submissions-header h2 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.export-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #059669;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.export-button:hover {
  background: #047857;
}

/* 表格样式 */
.submissions-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8fafc;
}

th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  border-bottom: 1px solid #e5e7eb;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
  font-size: 0.875rem;
}

.submission-row:hover {
  background: #f8fafc;
}

/* 学生信息 */
.student-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.student-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.student-name {
  font-weight: 500;
  color: #1e293b;
}

/* 状态标签 */
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-submitted {
  background: #dcfce7;
  color: #166534;
}

.status-unsubmitted {
  background: #fef3c7;
  color: #92400e;
}

/* 进度条 */
.progress-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  min-width: 80px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #059669);
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.75rem;
  color: #6b7280;
  white-space: nowrap;
}

/* 评分标签 */
.grade-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.grade-graded {
  background: #dcfce7;
  color: #166534;
}

.grade-ungraded {
  background: #fef3c7;
  color: #92400e;
}

.grade-na {
  background: #f3f4f6;
  color: #6b7280;
}

/* 分数 */
.score {
  font-weight: 600;
  color: #059669;
}

.no-score, .no-submit {
  color: #9ca3af;
}

/* 操作按钮 */
.actions {
  display: flex;
  gap: 0.5rem;
}

.view-button, .grade-button {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-button {
  background: #e0f2fe;
  color: #0369a1;
}

.view-button:hover {
  background: #bae6fd;
}

.grade-button {
  background: #fef3c7;
  color: #92400e;
}

.grade-button:hover {
  background: #fde68a;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  color: #64748b;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(100, 116, 139, 0.3);
  border-top: 3px solid #64748b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.detail-modal {
  background: white;
  border-radius: 12px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.close-button {
  width: 40px;
  height: 40px;
  border: none;
  background: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s ease;
}

.close-button:hover {
  background: #e5e7eb;
}

.modal-body {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

/* 提交元信息 */
.submission-meta {
  background: #f8fafc;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.meta-item {
  color: #374151;
  font-size: 0.875rem;
}

.meta-item strong {
  color: #1e293b;
}

.graded {
  color: #059669;
  font-weight: 500;
}

.ungraded {
  color: #d97706;
  font-weight: 500;
}

/* 题目详情 */
.problems-section h4 {
  color: #1e293b;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.problem-detail {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.problem-header {
  background: #f8fafc;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
}

.problem-number {
  font-weight: 600;
  color: #1e293b;
}

.problem-score {
  color: #059669;
  font-weight: 500;
  font-size: 0.875rem;
}

.problem-content {
  padding: 1.5rem;
}

.problem-text, .student-answer, .grading-result {
  margin-bottom: 1.5rem;
}

.problem-text strong, .student-answer strong, .grading-result strong {
  display: block;
  margin-bottom: 0.5rem;
  color: #374151;
  font-size: 0.875rem;
}

.answer-content, .result-content {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 1rem;
  margin-top: 0.5rem;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.no-answer {
  color: #9ca3af;
  font-style: italic;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 6px;
  text-align: center;
}

/* Markdown内容样式 */
:deep(.answer-content *),
:deep(.result-content *) {
  text-align: left;
}

:deep(.answer-content h1),
:deep(.answer-content h2),
:deep(.answer-content h3),
:deep(.result-content h1),
:deep(.result-content h2),
:deep(.result-content h3) {
  color: #1f2937;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  text-align: left;
}

:deep(.answer-content code),
:deep(.result-content code) {
  background: #f3f4f6;
  padding: 0.125rem 0.25rem;
  border-radius: 4px;
  font-size: 0.875em;
}

:deep(.answer-content pre),
:deep(.result-content pre) {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  overflow-x: auto;
  margin: 1rem 0;
}

:deep(.answer-content table),
:deep(.result-content table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1rem 0;
}

:deep(.answer-content th),
:deep(.answer-content td),
:deep(.result-content th),
:deep(.result-content td) {
  border: 1px solid #e5e7eb;
  padding: 0.5rem;
  text-align: left;
}

:deep(.answer-content th),
:deep(.result-content th) {
  background: #f9fafb;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-content {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .nav-left {
    flex-direction: column;
    gap: 1rem;
  }

  .main-content {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }

  .submissions-table {
    font-size: 0.75rem;
  }

  .modal-overlay {
    padding: 1rem;
  }

  .submission-meta {
    grid-template-columns: 1fr;
  }
}
</style>
