<template>
  <div class="problem-generation">
    <div class="page-header">
      <h1><i class="bi bi-magic me-2"></i>智能题目生成</h1>
      <p>基于AI的智能题目生成系统，可根据需求自动生成各类型题目</p>
    </div>

    <div class="row">
      <div class="col-md-8 mx-auto">
        <div class="card">
          <div class="card-header bg-light">
            <h5 class="mb-0">生成题目配置</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="generateProblems">
              <div class="row">
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="subject" class="form-label">学科领域</label>
                    <select class="form-select" id="subject" v-model="formData.subject" required>
                      <option value="计算机">计算机</option>
                      <option value="数学">数学</option>
                      <option value="物理">物理</option>
                      <option value="化学">化学</option>
                      <option value="生物">生物</option>
                      <option value="语文">语文</option>
                      <option value="英语">英语</option>
                    </select>
                  </div>
                  
                  <div class="mb-3">
                    <label for="difficulty" class="form-label">难度级别</label>
                    <select class="form-select" id="difficulty" v-model="formData.difficulty" required>
                      <option value="简单">简单</option>
                      <option value="中等">中等</option>
                      <option value="困难">困难</option>
                    </select>
                  </div>
                  
                  <div class="mb-3">
                    <label for="pattern_type" class="form-label">生成模式</label>
                    <select class="form-select" id="pattern_type" v-model="formData.pattern_type" required>
                      <option value="从上传题库中抽取">从上传题库中抽取</option>
                      <option value="参考资料自动生成">参考资料自动生成</option>
                    </select>
                  </div>
                </div>
                
                <div class="col-md-6">
                  <div class="mb-3">
                    <label class="form-label">题目类型与数量</label>
                    <div class="input-group mb-2">
                      <span class="input-group-text">选择题</span>
                      <input type="number" class="form-control" v-model.number="formData.choice" min="0">
                    </div>
                    <div class="input-group mb-2">
                      <span class="input-group-text">判断题</span>
                      <input type="number" class="form-control" v-model.number="formData.true_false" min="0">
                    </div>
                    <div class="input-group mb-2">
                      <span class="input-group-text">填空题</span>
                      <input type="number" class="form-control" v-model.number="formData.gap_filling" min="0">
                    </div>
                    <div class="input-group mb-2">
                      <span class="input-group-text">编程题</span>
                      <input type="number" class="form-control" v-model.number="formData.programming" min="0">
                    </div>
                    <div class="form-text">输入0表示不生成该类型题目</div>
                  </div>
                  
                  <div class="mb-3">
                    <label for="file" class="form-label">上传题库文件</label>
                    <input 
                      type="file" 
                      class="form-control" 
                      id="file" 
                      @change="handleFileChange"
                      accept=".txt"
                      :required="formData.pattern_type === '从上传题库中抽取'"
                    >
                    <div class="form-text">支持TXT格式的题库文件</div>
                  </div>
                </div>
              </div>
              
              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary" :disabled="isGenerating">
                  <span v-if="isGenerating" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="bi bi-magic me-1"></i>
                  {{ isGenerating ? '生成中...' : '生成题目' }}
                </button>
                <router-link to="/" class="btn btn-outline-secondary">
                  <i class="bi bi-arrow-left me-1"></i>返回首页
                </router-link>
              </div>
            </form>
          </div>
        </div>
        
        <!-- 生成结果 -->
        <div class="card mt-4" v-show="showResult">
          <div class="card-header bg-light">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="mb-0">生成结果</h5>
              <button class="btn btn-sm btn-outline-secondary" @click="printResult">
                <i class="bi bi-printer me-1"></i>打印
              </button>
            </div>
          </div>
          <div class="card-body">
            <div v-if="isGenerating" class="loading-spinner text-center">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">加载中...</span>
              </div>
              <p class="mt-2">AI正在生成题目，请稍候...</p>
            </div>
            
            <div v-else-if="generatedContent" class="result-container markdown-content" v-html="generatedContent">
            </div>
            
            <div v-else-if="errorMessage" class="alert alert-danger">
              {{ errorMessage }}
            </div>
            
            <div v-if="generatedContent && !isGenerating" class="mt-3 text-end">
              <button class="btn btn-success me-2" @click="copyResult">
                <i class="bi bi-clipboard me-1"></i>复制结果
              </button>
              <button class="btn btn-primary" @click="showSaveModal">
                <i class="bi bi-save me-1"></i>保存为作业
              </button>
            </div>
          </div>
        </div>
        
        <!-- 使用说明 -->
        <div class="card mt-4">
          <div class="card-header bg-light">
            <h5 class="mb-0">使用说明</h5>
          </div>
          <div class="card-body">
            <p>智能题目生成系统使用指南：</p>
            <ol>
              <li>选择学科领域和难度级别</li>
              <li>选择生成模式：从上传题库抽取或自动生成</li>
              <li>输入各类型题目的数量，输入0表示不生成该类型</li>
              <li>上传题库文件（TXT格式）</li>
              <li>点击"生成题目"按钮开始生成</li>
            </ol>
            <div class="alert alert-info">
              <i class="bi bi-info-circle me-1"></i>提示：生成的题目可以直接保存为作业，或复制结果用于其他用途。每种题型数量建议不超过5个，以保证生成质量。
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 保存作业模态框 -->
    <div class="modal fade" id="saveAssignmentModal" tabindex="-1" ref="saveModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">保存为作业</h5>
            <button type="button" class="btn-close" @click="closeSaveModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveAssignment">
              <div class="mb-3">
                <label for="assignmentTitle" class="form-label">作业标题</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="assignmentTitle" 
                  v-model="assignmentData.title"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="courseSelect" class="form-label">选择课程</label>
                <select class="form-select" id="courseSelect" v-model="assignmentData.course_id" required>
                  <option value="" disabled>请选择课程...</option>
                  <option v-for="course in courses" :key="course.id" :value="course.id">
                    {{ course.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label for="assignmentDescription" class="form-label">作业描述</label>
                <textarea 
                  class="form-control" 
                  id="assignmentDescription" 
                  v-model="assignmentData.description"
                  rows="3"
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="dueDate" class="form-label">截止日期（可选）</label>
                <input 
                  type="date" 
                  class="form-control" 
                  id="dueDate" 
                  v-model="assignmentData.due_date"
                >
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeSaveModal">取消</button>
            <button type="button" class="btn btn-primary" @click="saveAssignment" :disabled="isSaving">
              <span v-if="isSaving" class="spinner-border spinner-border-sm me-2"></span>
              {{ isSaving ? '保存中...' : '保存作业' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { workflowAPI } from '../utils/api'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css' // 导入代码高亮样式

export default {
  name: 'ProblemGeneration',
  setup() {
    const isGenerating = ref(false)
    const isSaving = ref(false)
    const showResult = ref(false)
    const generatedContent = ref('')
    const errorMessage = ref('')
    const selectedFile = ref(null)
    const courses = ref([])
    const saveModal = ref(null)

    // 初始化 markdown-it 实例
    const md = new MarkdownIt({
      html: true,        // 启用 HTML 标签
      breaks: true,      // 转换段落里的 '\n' 到 <br>
      linkify: true,     // 自动将URL文本转换为链接
      typographer: true, // 启用一些语言中立的替换 + 引号美化
      highlight: function (str, lang) {
        // 代码高亮
        if (lang && hljs.getLanguage(lang)) {
          try {
            return '<pre class="hljs"><code>' +
                   hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
                   '</code></pre>'
          } catch (__) {}
        }
        
        // 使用通用的转义
        return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>'
      }
    })

    const formData = reactive({
      subject: '计算机',
      difficulty: '中等',
      pattern_type: '从上传题库中抽取',
      choice: 1,
      true_false: 1,
      gap_filling: 1,
      programming: 1
    })

    const assignmentData = reactive({
      title: '',
      course_id: '',
      description: '',
      due_date: ''
    })

    const validateQuestionCounts = () => {
      const total = formData.choice + formData.true_false + formData.gap_filling + formData.programming
      if (total <= 0) {
        alert('请至少选择一种题型并输入数量')
        return false
      }
      return true
    }

    const handleFileChange = (event) => {
      selectedFile.value = event.target.files[0]
    }

    const generateProblems = async () => {
      if (!validateQuestionCounts()) {
        return
      }

      if (formData.pattern_type === '从上传题库中抽取' && !selectedFile.value) {
        alert('请上传题库文件')
        return
      }

      isGenerating.value = true
      showResult.value = true
      generatedContent.value = ''
      errorMessage.value = ''

      try {
        const formDataToSend = new FormData()
        Object.keys(formData).forEach(key => {
          formDataToSend.append(key, formData[key])
        })
        
        if (selectedFile.value) {
          formDataToSend.append('file', selectedFile.value)
        }

        const response = await workflowAPI.runWorkflow(formDataToSend)

        if (response.data.error) {
          errorMessage.value = response.data.error
        } else if (response.data.data?.outputs?.output1) {
          // 使用 markdown-it 渲染 Markdown
          const output = response.data.data.outputs.output1
          generatedContent.value = md.render(output)
          enhanceResultContent()
        } else {
          errorMessage.value = '未生成任何结果，请调整参数后重试。'
        }
      } catch (error) {
        console.error('生成题目失败:', error)
        errorMessage.value = `请求失败: ${error.response?.data?.message || error.message}`
      } finally {
        isGenerating.value = false
      }
    }

    // 增强结果内容展示效果
    const enhanceResultContent = () => {
      // 添加表格样式
      const tableStyles = `
        <style>
          .markdown-content table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            text-align: left;
          }
          .markdown-content table * {
            text-align: left;
          }
          .markdown-content th, .markdown-content td {
            border: 1px solid #e1e1e1;
            padding: 8px 12px;
            text-align: left;
          }
          .markdown-content th {
            background-color: #f5f5f5;
            font-weight: 600;
            text-align: left;
          }
          .markdown-content tr {
            text-align: left;
          }
          .markdown-content tr:nth-child(even) {
            background-color: #f9f9f9;
          }
        </style>
      `
      
      generatedContent.value = tableStyles + generatedContent.value
    }

    const copyResult = async () => {
      try {
        const textContent = document.querySelector('.result-container').innerText
        await navigator.clipboard.writeText(textContent)
        alert('结果已复制到剪贴板')
      } catch (error) {
        console.error('复制失败:', error)
        alert('复制失败，请手动选择并复制')
      }
    }

    const printResult = () => {
      const printWindow = window.open('', '_blank')
      const content = generatedContent.value
      
      printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>智能生成题目</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1 { font-size: 1.8rem; text-align: left; }
            h2 { font-size: 1.5rem; color: #3c6e71; margin-top: 20px; text-align: left; }
            * { text-align: left; }
          </style>
        </head>
        <body>
          ${content}
        </body>
        </html>
      `)
      
      printWindow.document.close()
      printWindow.focus()
      setTimeout(() => {
        printWindow.print()
      }, 500)
    }

    const loadCourses = async () => {
      try {
        const response = await workflowAPI.getTeacherCourses()
        courses.value = response.data.courses || []
      } catch (error) {
        console.error('获取课程列表失败:', error)
        // 使用模拟数据
        courses.value = [
          { id: 1, name: '高等数学' },
          { id: 2, name: '线性代数' },
          { id: 3, name: '数据结构' }
        ]
      }
    }

    const showSaveModal = () => {
      loadCourses()
      const modal = new bootstrap.Modal(saveModal.value)
      modal.show()
    }

    const closeSaveModal = () => {
      const modal = bootstrap.Modal.getInstance(saveModal.value)
      if (modal) {
        modal.hide()
      }
    }

    const saveAssignment = async () => {
      if (!assignmentData.title || !assignmentData.course_id) {
        alert('请填写必要信息')
        return
      }

      isSaving.value = true
      try {
        const response = await workflowAPI.saveGeneratedAssignment({
          title: assignmentData.title,
          course_id: assignmentData.course_id,
          description: assignmentData.description,
          due_date: assignmentData.due_date,
          problem_content: generatedContent.value
        })

        if (response.data.success) {
          closeSaveModal()
          generatedContent.value = `
            <div class="alert alert-success">
              <h4 style="text-align: left;"><i class="bi bi-check-circle me-2"></i>作业保存成功!</h4>
              <p style="text-align: left;">作业已成功添加到课程: ${response.data.course_name}</p>
            </div>
          `
        } else {
          alert(`保存失败: ${response.data.error || '未知错误'}`)
        }
      } catch (error) {
        console.error('保存作业失败:', error)
        alert('保存失败，请稍后再试')
      } finally {
        isSaving.value = false
      }
    }

    // 添加链接处理：自动为外部链接添加 target="_blank" 属性
    onMounted(() => {
      document.addEventListener('click', (e) => {
        const link = e.target.closest('a')
        if (link && link.hostname !== window.location.hostname) {
          link.setAttribute('target', '_blank')
          link.setAttribute('rel', 'noopener noreferrer')
        }
      })
    })

    return {
      formData,
      assignmentData,
      isGenerating,
      isSaving,
      showResult,
      generatedContent,
      errorMessage,
      courses,
      saveModal,
      handleFileChange,
      generateProblems,
      copyResult,
      printResult,
      showSaveModal,
      closeSaveModal,
      saveAssignment
    }
  }
}
</script>

<style scoped>
.page-header {
  text-align: center;
  margin-bottom: 30px;
  border-bottom: 2px solid #3c6e71;
  padding-bottom: 20px;
}

.page-header h1 {
  color: #2c3e50;
  font-weight: 600;
}

.page-header p {
  color: #7f8c8d;
  font-size: 16px;
}

.result-container {
  border: 1px solid #e9ecef;
  border-radius: 0.25rem;
  padding: 15px;
  max-height: 500px;
  overflow-y: auto;
  background-color: #f8f9fa;
  text-align: left;
}

.loading-spinner {
  margin: 20px 0;
}

/* Markdown 渲染样式 */
:deep(.markdown-content) {
  line-height: 1.6;
  text-align: left;
}

:deep(.markdown-content *) {
  text-align: left;
}

:deep(.markdown-content h1) {
  font-size: 1.8rem;
  margin: 20px 0 15px;
  color: #3c6e71;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 8px;
  text-align: left;
}

:deep(.markdown-content h2) {
  font-size: 1.5rem;
  margin: 20px 0 12px;
  color: #2c3e50;
  padding-bottom: 5px;
  border-bottom: 1px solid #f0f0f0;
  text-align: left;
}

:deep(.markdown-content h3) {
  font-size: 1.3rem;
  margin: 16px 0 10px;
  color: #2c3e50;
  text-align: left;
}

:deep(.markdown-content p) {
  margin: 10px 0;
  text-align: left;
}

:deep(.markdown-content ul),
:deep(.markdown-content ol) {
  padding-left: 25px;
  margin: 10px 0;
  text-align: left;
}

:deep(.markdown-content li) {
  margin-bottom: 5px;
  text-align: left;
}

:deep(.markdown-content a) {
  color: #3c6e71;
  text-decoration: none;
}

:deep(.markdown-content a:hover) {
  text-decoration: underline;
}

:deep(.markdown-content blockquote) {
  border-left: 4px solid #e0e0e0;
  padding: 10px 15px;
  margin: 15px 0;
  background-color: #f8f9fa;
  color: #666;
  text-align: left;
}

:deep(.markdown-content code:not(.hljs)) {
  background-color: #f5f5f5;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9em;
}

:deep(.markdown-content pre) {
  background-color: #f8f9fa;
  border-radius: 6px;
  margin: 15px 0;
  overflow-x: auto;
  text-align: left;
}

:deep(.markdown-content .hljs) {
  padding: 15px;
  border-radius: 5px;
  font-family: 'Courier New', Courier, monospace;
}

:deep(.markdown-content strong) {
  color: #3c6e71;
  font-weight: 600;
}

:deep(.markdown-content em) {
  font-style: italic;
}

:deep(.markdown-content img) {
  max-width: 100%;
  border-radius: 5px;
  margin: 10px 0;
}

:deep(.markdown-content hr) {
  border: 0;
  border-top: 1px solid #eee;
  margin: 20px 0;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style> 