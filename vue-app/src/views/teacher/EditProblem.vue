<template>
  <div class="edit-problem-page">
    <!-- 顶部导航栏 -->
    <div class="top-navigation">
      <div class="nav-content">
        <div class="nav-left">
          <router-link 
            :to="problem ? `/teacher/assignments/${problem.assignment_id}/edit` : '/teacher/courses'" 
            class="back-button"
          >
            <i class="bi bi-arrow-left"></i>
            <span>返回作业</span>
          </router-link>
          <div class="breadcrumb">
            <span class="breadcrumb-item">{{ problem?.assignment_title || '作业' }}</span>
            <i class="bi bi-chevron-right"></i>
            <span class="breadcrumb-current">编辑题目 {{ problem?.order }}</span>
          </div>
        </div>
        <div class="nav-right">
          <button 
            class="save-button"
            @click="updateProblem"
            :disabled="isSaving"
          >
            <i class="bi bi-check-lg" v-if="!isSaving"></i>
            <div class="spinner" v-if="isSaving"></div>
            <span>{{ isSaving ? '保存中...' : '保存更改' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content" v-if="!isLoading">
      <div class="content-container">
        <!-- 编辑面板 -->
        <div class="edit-panel">
          <div class="panel-header">
            <h2><i class="bi bi-pencil-square"></i>编辑题目</h2>
            <div class="view-toggle">
              <button 
                class="toggle-btn"
                :class="{ active: viewMode === 'edit' }"
                @click="viewMode = 'edit'"
              >
                <i class="bi bi-pencil"></i>编辑
              </button>
              <button 
                class="toggle-btn"
                :class="{ active: viewMode === 'preview' }"
                @click="viewMode = 'preview'"
              >
                <i class="bi bi-eye"></i>预览
              </button>
            </div>
          </div>

          <!-- 编辑模式 -->
          <div v-show="viewMode === 'edit'" class="edit-form">
            <div class="form-section">
              <label class="form-label">
                <i class="bi bi-file-text"></i>
                题目内容
                <span class="required">*</span>
              </label>
              <div class="editor-container">
                <textarea 
                  v-model="problem.problem_text"
                  class="content-editor"
                  placeholder="请输入题目内容，支持 Markdown 格式..."
                  :key="problem?.id"
                ></textarea>
                <div class="editor-hint">
                  <i class="bi bi-info-circle"></i>
                  支持 Markdown 格式，包括代码块、表格、链接等
                </div>
              </div>
            </div>

            <div class="form-section">
              <label class="form-label">
                <i class="bi bi-lightbulb"></i>
                参考答案
              </label>
              <div class="editor-container">
                <textarea 
                  v-model="problem.reference_answer"
                  class="content-editor answer-editor"
                  placeholder="提供标准答案，学生将看不到此内容..."
                  :key="'answer-' + problem?.id"
                ></textarea>
                <div class="editor-hint">
                  <i class="bi bi-shield-lock"></i>
                  此内容仅对教师可见，用于AI自动评分参考
                </div>
              </div>
            </div>

            <div class="form-section">
              <label class="form-label">
                <i class="bi bi-clipboard-check"></i>
                评分标准
              </label>
              <div class="editor-container">
                <textarea 
                  v-model="problem.grading_criteria"
                  class="content-editor criteria-editor"
                  placeholder="描述评分标准，AI批改系统将参考这些标准..."
                  :key="'criteria-' + problem?.id"
                ></textarea>
                <div class="editor-hint">
                  <i class="bi bi-gear"></i>
                  例如：代码功能实现（50分）、代码风格（30分）、注释完整性（20分）
                </div>
              </div>
            </div>

            <div class="form-section compact">
              <label class="form-label">
                <i class="bi bi-hash"></i>
                题目顺序
              </label>
              <input 
                type="number" 
                v-model.number="problem.order"
                class="order-input"
                min="1"
                :key="'order-' + problem?.id"
              >
            </div>
          </div>

          <!-- 预览模式 -->
          <div v-show="viewMode === 'preview'" class="preview-content">
            <div class="preview-section">
              <h3><i class="bi bi-eye"></i>题目预览</h3>
              <div class="preview-card">
                <div class="question-header">
                  <span class="question-number">第 {{ parseInt(problem?.order) || 1 }} 题</span>
                </div>
                <div class="question-content" v-html="renderMarkdown(problem?.problem_text || '暂无题目内容')"></div>
              </div>
            </div>

            <div class="preview-section" v-if="problem?.reference_answer">
              <h3><i class="bi bi-lightbulb-fill"></i>参考答案</h3>
              <div class="preview-card answer-card">
                <div class="answer-content" v-html="renderMarkdown(problem.reference_answer)"></div>
              </div>
            </div>

            <div class="preview-section" v-if="problem?.grading_criteria">
              <h3><i class="bi bi-clipboard-check-fill"></i>评分标准</h3>
              <div class="preview-card criteria-card">
                <div class="criteria-content" v-html="renderMarkdown(problem.grading_criteria)"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>正在加载题目信息...</p>
    </div>

    <!-- 快速保存提示 -->
    <div v-if="showSaveNotification" class="save-notification">
      <i class="bi bi-check-circle-fill"></i>
      <span>更改已保存</span>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick, computed, watch, onUnmounted } from 'vue'
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
  name: 'EditProblem',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const problemId = route.params.id
    
    const problem = ref(null)
    const isLoading = ref(true)
    const isSaving = ref(false)
    const viewMode = ref('edit')
    const showSaveNotification = ref(false)

    const loadProblem = async () => {
      try {
        const response = await teacherAPI.getProblem(problemId)
        if (response.data.success) {
          problem.value = response.data.problem
          // 确保order字段是数字类型
          if (problem.value.order) {
            problem.value.order = parseInt(problem.value.order)
          }
        } else {
          throw new Error(response.data.message || '加载题目失败')
        }
      } catch (error) {
        console.error('加载题目失败:', error)
        alert('加载题目失败')
        router.push('/teacher/courses')
      } finally {
        isLoading.value = false
      }
    }

    const updateProblem = async () => {
      if (!problem.value?.problem_text?.trim()) {
        alert('请输入题目内容')
        return
      }

      // 验证题目顺序
      const order = parseInt(problem.value.order)
      if (!order || order < 1) {
        alert('题目顺序必须是大于0的整数')
        return
      }

      isSaving.value = true
      try {
        const updateData = {
          problem_text: problem.value.problem_text.trim(),
          reference_answer: problem.value.reference_answer?.trim() || null,
          grading_criteria: problem.value.grading_criteria?.trim() || null,
          order: order
        }
        
        console.log('更新题目数据:', updateData)
        
        const response = await teacherAPI.updateProblem(problemId, updateData)
        
        console.log('更新响应:', response.data)
        
        if (response.data.success) {
          // 更新本地数据确保同步
          problem.value.order = order
          console.log('题目顺序更新成功，新顺序:', order)
          showSaveNotification.value = true
          setTimeout(() => {
            showSaveNotification.value = false
          }, 3000)
        } else {
          throw new Error(response.data.message || '保存失败')
        }
      } catch (error) {
        console.error('保存题目失败:', error)
        alert('保存题目失败')
      } finally {
        isSaving.value = false
      }
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

    // 键盘快捷键
    const handleKeyboard = (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key === 's') {
        event.preventDefault()
        updateProblem()
      }
    }

    onMounted(() => {
      loadProblem()
      document.addEventListener('keydown', handleKeyboard)
    })

    // 组件卸载时清理事件监听器
    onUnmounted(() => {
      document.removeEventListener('keydown', handleKeyboard)
    })

    return {
      problem,
      isLoading,
      isSaving,
      viewMode,
      showSaveNotification,
      updateProblem,
      renderMarkdown
    }
  }
}
</script>

<style scoped>
.edit-problem-page {
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
  max-width: 1200px;
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

.save-button {
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

.save-button:hover:not(:disabled) {
  background: #334155;
  transform: translateY(-1px);
}

.save-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 主要内容区域 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.content-container {
  display: flex;
  justify-content: center;
}

/* 编辑面板 */
.edit-panel {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 900px;
}

.panel-header {
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #64748b 0%, #475569 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.view-toggle {
  display: flex;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 4px;
}

.toggle-btn {
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.8);
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.toggle-btn.active {
  background: white;
  color: #64748b;
  font-weight: 500;
}

/* 编辑表单 */
.edit-form {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

.form-section {
  margin-bottom: 2rem;
}

.form-section.compact {
  margin-bottom: 1.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
}

.required {
  color: #dc2626;
}

.editor-container {
  position: relative;
}

.content-editor {
  width: 100%;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  resize: vertical;
  transition: all 0.2s ease;
  background: #fafafa;
}

.content-editor:focus {
  outline: none;
  border-color: #64748b;
  background: white;
  box-shadow: 0 0 0 3px rgba(100, 116, 139, 0.1);
}

.content-editor {
  min-height: 200px;
}

.answer-editor {
  min-height: 150px;
}

.criteria-editor {
  min-height: 120px;
}

.editor-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #64748b;
}

.order-input {
  width: 100px;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.order-input:focus {
  outline: none;
  border-color: #64748b;
  box-shadow: 0 0 0 3px rgba(100, 116, 139, 0.1);
}

/* 预览内容 */
.preview-content {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

.preview-section {
  margin-bottom: 2rem;
}

.preview-section h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.preview-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
}

.question-header {
  margin-bottom: 1rem;
}

.question-number {
  background: #64748b;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.answer-card {
  background: #fef3c7;
  border-color: #f59e0b;
}

.criteria-card {
  background: #ecfdf5;
  border-color: #10b981;
}

/* 加载和通知状态 */
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

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.save-notification {
  position: fixed;
  top: 100px;
  right: 2rem;
  background: #475569;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px rgba(71, 85, 105, 0.4);
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Markdown 内容样式 */
:deep(.question-content),
:deep(.answer-content),
:deep(.criteria-content) {
  line-height: 1.6;
  color: #374151;
}

:deep(.question-content h1),
:deep(.question-content h2),
:deep(.question-content h3),
:deep(.answer-content h1),
:deep(.answer-content h2),
:deep(.answer-content h3),
:deep(.criteria-content h1),
:deep(.criteria-content h2),
:deep(.criteria-content h3) {
  color: #1f2937;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

:deep(.question-content code),
:deep(.answer-content code),
:deep(.criteria-content code) {
  background: #f3f4f6;
  padding: 0.125rem 0.25rem;
  border-radius: 4px;
  font-size: 0.875em;
}

:deep(.question-content pre),
:deep(.answer-content pre),
:deep(.criteria-content pre) {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  overflow-x: auto;
  margin: 1rem 0;
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

  .edit-form,
  .preview-content {
    padding: 1rem;
  }

  .view-toggle {
    flex: 1;
  }

  .toggle-btn {
    flex: 1;
    justify-content: center;
  }
}
</style>
