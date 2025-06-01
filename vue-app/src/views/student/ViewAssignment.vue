<template>
  <div class="student-view-assignment">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <h1><i class="bi bi-file-earmark-text me-2"></i>{{ assignment.title }}</h1>
        <div>
          <router-link to="/student/dashboard" class="btn btn-outline-secondary">
            <i class="bi bi-arrow-left me-1"></i>返回主页
          </router-link>
        </div>
      </div>
      <p class="text-muted">{{ assignment.course_name }} - {{ assignment.description || '暂无描述' }}</p>
    </div>

    <!-- 作业状态卡片 -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h5 class="card-title mb-1">作业状态</h5>
                <p class="card-text text-muted">
                  {{ assignment.due_date ? `截止日期: ${formatDate(assignment.due_date)}` : '无截止日期' }}
                </p>
              </div>
              <div class="text-center">
                <span class="badge rounded-pill p-2" :class="getStatusBadgeClass()">
                  {{ getStatusText() }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h5 class="card-title mb-1">作业完成情况</h5>
                <p class="card-text text-muted">
                  共 {{ problems.length }} 道题目
                </p>
              </div>
              <div class="text-center">
                <div class="progress" style="width: 100px; height: 20px;">
                  <div class="progress-bar" :class="getProgressBarClass()" 
                       role="progressbar" :style="`width: ${completionPercentage}%;`" 
                       :aria-valuenow="completionPercentage" aria-valuemin="0" aria-valuemax="100">
                    {{ completionPercentage }}%
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
      <p class="mt-2">正在加载作业内容...</p>
    </div>

    <!-- 作业内容 -->
    <div v-else class="row">
      <div class="col-md-12">
        <!-- 已评分提示 -->
        <div v-if="submission && submission.is_graded" class="alert alert-success mb-4">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h5 class="alert-heading"><i class="bi bi-trophy me-2"></i>作业已评分</h5>
              <p class="mb-0">您已完成此作业并获得了评分。您仍然可以查看题目和您的答案。</p>
            </div>
            <div>
              <span class="score-display" :class="getScoreClass(submission.total_score)">
                {{ submission.total_score || 0 }}
              </span>
              <span class="text-muted">/100</span>
            </div>
          </div>
        </div>
        
        <!-- 题目表单 -->
        <form @submit.prevent="submitAllAnswers">
          <div class="accordion" id="problem-accordion">
            <div v-for="(problem, index) in problems" :key="problem.id" 
                 class="accordion-item problem-card mb-4">
              <h2 class="accordion-header" :id="`heading-${problem.id}`">
                <button class="accordion-button" :class="{ collapsed: index !== 0 }" 
                        type="button" data-bs-toggle="collapse" 
                        :data-bs-target="`#collapse-${problem.id}`" 
                        :aria-expanded="index === 0 ? 'true' : 'false'" 
                        :aria-controls="`collapse-${problem.id}`">
                  <div class="d-flex justify-content-between w-100 me-3">
                    <span>题目 {{ problem.order }}：{{ truncateText(stripHtml(problem.problem_text), 50) }}</span>
                    <span v-if="problem.score !== undefined" class="badge" :class="getScoreBadgeClass(problem.score)">
                      {{ problem.score }}分
                    </span>
                  </div>
                </button>
              </h2>
              <div :id="`collapse-${problem.id}`" class="accordion-collapse collapse" 
                   :class="{ show: index === 0 }" 
                   :aria-labelledby="`heading-${problem.id}`" 
                   data-bs-parent="#problem-accordion">
                <div class="accordion-body">
                  <div class="row">
                    <div class="col-md-12">
                      <!-- 题目内容 -->
                      <div class="card mb-3">
                        <div class="card-header">题目内容</div>
                        <div class="card-body">
                          <div class="markdown-preview" v-html="renderMarkdown(problem.problem_text)"></div>
                        </div>
                      </div>
                      
                      <!-- 我的答案 -->
                      <div class="card mb-3">
                        <div class="card-header">我的答案</div>
                        <div class="card-body">
                          <textarea 
                            class="form-control answer-textarea" 
                            v-model="answers[problem.id]" 
                            rows="8" 
                            placeholder="在此输入您的答案..."
                            :disabled="submission && submission.is_graded">
                          </textarea>
                        </div>
                      </div>
                      
                      <!-- 评分结果 -->
                      <div v-if="problem.grading_result" class="card mb-3">
                        <div class="card-header">评分结果</div>
                        <div class="card-body">
                          <div class="grading-result markdown-preview" v-html="renderMarkdown(problem.grading_result)"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 提交按钮 -->
          <div class="d-grid mt-4" v-if="!submission || !submission.is_graded">
            <button type="submit" class="btn btn-primary btn-lg" :disabled="isSubmitting">
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-send me-1"></i>
              {{ isSubmitting ? '正在提交...' : '提交全部答案' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 提交结果模态框 -->
    <div v-if="showResultModal" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">提交结果</h5>
            <button type="button" class="btn-close" @click="closeResultModal"></button>
          </div>
          <div class="modal-body">
            <div v-if="submissionResult.success" class="text-center">
              <i class="bi bi-check-circle text-success display-4 mb-3"></i>
              <h5>提交成功！</h5>
              <p>{{ submissionResult.message }}</p>
            </div>
            <div v-else class="text-center">
              <i class="bi bi-x-circle text-danger display-4 mb-3"></i>
              <h5>提交失败</h5>
              <p>{{ submissionResult.message }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="closeResultModal">确定</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../utils/api'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

export default {
  name: 'StudentViewAssignment',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // 配置markdown解析器
    const md = new MarkdownIt({
      html: true,
      breaks: true,
      linkify: true,
      typographer: true,
      highlight: function (str, lang) {
        if (lang && hljs.getLanguage(lang)) {
          try {
            return '<pre class="hljs"><code>' +
                   hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
                   '</code></pre>';
          } catch (__) {}
        }
        return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
      }
    })
    
    const isLoading = ref(true)
    const isSubmitting = ref(false)
    const assignment = ref({})
    const problems = ref([])
    const submission = ref(null)
    const answers = reactive({})
    const submissionResult = reactive({
      success: false,
      message: ''
    })
    const showResultModal = ref(false)

    // 计算属性
    const completionPercentage = computed(() => {
      if (!problems.value.length) return 0
      const completed = Object.keys(answers).filter(key => answers[key] && answers[key].trim()).length
      return Math.round((completed / problems.value.length) * 100)
    })

    // 加载作业详情
    const loadAssignmentDetail = async () => {
      try {
        isLoading.value = true
        const assignmentId = route.params.id
        const response = await api.get(`/student/assignments/${assignmentId}`)
        
        if (response.data.success) {
          const data = response.data.data
          assignment.value = data.assignment
          problems.value = data.problems
          submission.value = data.submission
          
          // 初始化答案
          problems.value.forEach(problem => {
            answers[problem.id] = problem.answer || ''
          })
        } else {
          throw new Error(response.data.message || '加载失败')
        }
      } catch (error) {
        console.error('加载作业详情失败:', error)
        alert('加载作业详情失败: ' + error.message)
        router.push('/student/dashboard')
      } finally {
        isLoading.value = false
      }
    }

    // 提交所有答案
    const submitAllAnswers = async () => {
      try {
        // 验证是否有答案
        const hasAnswers = Object.values(answers).some(answer => answer && answer.trim())
        if (!hasAnswers) {
          alert('请至少回答一道题目')
          return
        }

        isSubmitting.value = true
        
        const assignmentId = route.params.id
        const response = await api.post(`/student/assignments/${assignmentId}/submit`, {
          answers: answers
        })
        
        if (response.data.success) {
          submissionResult.success = true
          submissionResult.message = response.data.message || '作业提交成功'
          
          // 刷新页面数据
          await loadAssignmentDetail()
        } else {
          throw new Error(response.data.message || '提交失败')
        }
      } catch (error) {
        console.error('提交作业失败:', error)
        submissionResult.success = false
        submissionResult.message = error.response?.data?.message || error.message || '提交失败'
      } finally {
        isSubmitting.value = false
        // 显示结果模态框 - 使用Vue的响应式变量而不是bootstrap
        showResultModal.value = true
      }
    }

    // 辅助方法
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    const renderMarkdown = (text) => {
      if (!text) return ''
      return md.render(text)
    }

    const stripHtml = (html) => {
      const doc = new DOMParser().parseFromString(html, 'text/html')
      return doc.body.textContent || ""
    }

    const truncateText = (text, length) => {
      return text.length > length ? text.substring(0, length) + '...' : text
    }

    const getStatusBadgeClass = () => {
      if (submission.value) {
        if (submission.value.is_graded) {
          return 'bg-success'
        } else {
          return 'bg-warning'
        }
      }
      return 'bg-danger'
    }

    const getStatusText = () => {
      if (submission.value) {
        if (submission.value.is_graded) {
          return '已评分'
        } else {
          return '已提交，待评分'
        }
      }
      return '未提交'
    }

    const getProgressBarClass = () => {
      const percentage = completionPercentage.value
      if (percentage === 100) return 'bg-success'
      if (percentage >= 50) return 'bg-warning'
      return 'bg-danger'
    }

    const getScoreClass = (score) => {
      if (score >= 80) return 'score-high'
      if (score >= 60) return 'score-medium'
      return 'score-low'
    }

    const getScoreBadgeClass = (score) => {
      if (score >= 80) return 'bg-success'
      if (score >= 60) return 'bg-warning'
      return 'bg-danger'
    }

    const closeResultModal = () => {
      showResultModal.value = false
    }

    onMounted(() => {
      loadAssignmentDetail()
    })

    return {
      isLoading,
      isSubmitting,
      assignment,
      problems,
      submission,
      answers,
      submissionResult,
      completionPercentage,
      loadAssignmentDetail,
      submitAllAnswers,
      formatDate,
      renderMarkdown,
      stripHtml,
      truncateText,
      getStatusBadgeClass,
      getStatusText,
      getProgressBarClass,
      getScoreClass,
      getScoreBadgeClass,
      showResultModal,
      closeResultModal
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

.problem-card {
  border-left: 3px solid #3c6e71;
  margin-bottom: 20px;
}

.grading-result {
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  margin-top: 10px;
}

.score-display {
  font-size: 1.5rem;
  font-weight: bold;
}

.score-high {
  color: #28a745;
}

.score-medium {
  color: #fd7e14;
}

.score-low {
  color: #dc3545;
}

.answer-textarea {
  font-family: monospace;
  min-height: 200px;
  resize: vertical;
}

.markdown-preview {
  line-height: 1.6;
  text-align: left;
}

.markdown-preview * {
  text-align: left;
}

.markdown-preview h1,
.markdown-preview h2,
.markdown-preview h3,
.markdown-preview h4,
.markdown-preview h5,
.markdown-preview h6 {
  text-align: left;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.markdown-preview h1:first-child,
.markdown-preview h2:first-child,
.markdown-preview h3:first-child,
.markdown-preview h4:first-child,
.markdown-preview h5:first-child,
.markdown-preview h6:first-child {
  margin-top: 0;
}

.markdown-preview p {
  text-align: left;
  margin-bottom: 1rem;
}

.markdown-preview ul,
.markdown-preview ol {
  text-align: left;
  margin-bottom: 1rem;
  padding-left: 2rem;
}

.markdown-preview li {
  text-align: left;
  margin-bottom: 0.5rem;
}

.markdown-preview blockquote {
  text-align: left;
  border-left: 4px solid #ddd;
  padding-left: 1rem;
  margin: 1rem 0;
  color: #666;
  font-style: italic;
}

.markdown-preview pre {
  text-align: left;
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 0.375rem;
  overflow-x: auto;
  margin-bottom: 1rem;
}

.markdown-preview code {
  text-align: left;
  background-color: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875em;
}

.markdown-preview pre code {
  background-color: transparent;
  padding: 0;
  border-radius: 0;
}

.markdown-preview table {
  text-align: left;
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 1rem;
}

.markdown-preview th,
.markdown-preview td {
  text-align: left;
  border: 1px solid #ddd;
  padding: 0.5rem;
}

.markdown-preview th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.markdown-preview a {
  color: #007bff;
  text-decoration: none;
}

.markdown-preview a:hover {
  text-decoration: underline;
}

.markdown-preview img {
  max-width: 100%;
  height: auto;
  margin: 1rem 0;
}

.markdown-preview hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 2rem 0;
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

.btn:disabled {
  opacity: 0.65;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.progress {
  border-radius: 10px;
}

.progress-bar {
  border-radius: 10px;
  transition: width 0.3s ease;
}

.accordion-button:not(.collapsed) {
  background-color: #e7f3ff;
  color: #0a58ca;
}

.accordion-button:focus {
  border-color: #86b7fe;
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.badge {
  font-size: 0.8em;
}

.alert-success {
  border-color: #b3d7ff;
  background-color: #e7f3ff;
}

.modal-content {
  border-radius: 0.5rem;
}

.modal-header {
  border-bottom: 1px solid #dee2e6;
  border-radius: 0.5rem 0.5rem 0 0;
}

.modal-footer {
  border-top: 1px solid #dee2e6;
  border-radius: 0 0 0.5rem 0.5rem;
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
  
  .score-display {
    font-size: 1.2rem;
  }
}
</style>
