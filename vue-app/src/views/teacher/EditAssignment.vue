<template>
  <div class="edit-assignment">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <h1><i class="bi bi-file-earmark-text me-2"></i>编辑作业</h1>
        <div class="btn-group">
          <router-link 
            v-if="assignment"
            :to="`/teacher/assignments/${assignment.id}/submissions`" 
            class="btn btn-outline-success"
          >
            <i class="bi bi-people me-1"></i>查看提交
          </router-link>
          <router-link 
            :to="assignment ? `/teacher/courses/${assignment.course_id}` : '/teacher/courses'" 
            class="btn btn-outline-secondary"
          >
            <i class="bi bi-arrow-left me-1"></i>返回课程
          </router-link>
        </div>
      </div>
      <p class="text-muted" v-if="assignment">
        {{ assignment.course?.name }} - {{ assignment.title }}
      </p>
    </div>

    <div class="row" v-if="assignment">
      <div class="col-md-4">
        <div class="card mb-4">
          <div class="card-header bg-light">
            <h5 class="mb-0">作业信息</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="updateAssignment">
              <div class="mb-3">
                <label for="title" class="form-label">作业标题</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="title" 
                  v-model="formData.title"
                  required
                >
              </div>
              
              <div class="mb-3">
                <label for="description" class="form-label">作业描述</label>
                <textarea 
                  class="form-control" 
                  id="description" 
                  v-model="formData.description"
                  rows="3"
                ></textarea>
              </div>
              
              <div class="mb-3">
                <label for="due_date" class="form-label">截止日期</label>
                <input 
                  type="date" 
                  class="form-control" 
                  id="due_date" 
                  v-model="formData.due_date"
                >
              </div>
              
              <button 
                type="submit" 
                class="btn btn-primary w-100"
                :disabled="isSaving"
              >
                {{ isSaving ? '保存中...' : '保存作业信息' }}
              </button>
            </form>
          </div>
        </div>
        
        <div class="card mb-4">
          <div class="card-header bg-light">
            <h5 class="mb-0">作业统计</h5>
          </div>
          <div class="card-body">
            <div class="row text-center">
              <div class="col-6">
                <div class="stat-item">
                  <div class="stat-number">{{ problems.length }}</div>
                  <div class="stat-label">题目数量</div>
                </div>
              </div>
              <div class="col-6">
                <div class="stat-item">
                  <div class="stat-number">-</div>
                  <div class="stat-label">学生提交</div>
                </div>
              </div>
            </div>
            <div class="d-grid mt-3">
              <router-link 
                v-if="assignment"
                :to="`/teacher/assignments/${assignment.id}/submissions`" 
                class="btn btn-success"
              >
                <i class="bi bi-clipboard-check me-1"></i>查看学生提交
              </router-link>
            </div>
          </div>
        </div>
        
        <div class="card">
          <div class="card-header bg-light">
            <h5 class="mb-0">添加题目</h5>
          </div>
          <div class="card-body">
            <div class="d-grid gap-2">
              <button 
                class="btn btn-outline-primary"
                @click="showAddProblemModal = true"
              >
                <i class="bi bi-plus-circle me-1"></i>手动添加题目
              </button>
              
              <button 
                class="btn btn-outline-success"
                @click="showGenerateProblemModal = true"
              >
                <i class="bi bi-magic me-1"></i>智能生成题目
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-8">
        <div class="card">
          <div class="card-header bg-light">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="mb-0">题目列表</h5>
              <span class="badge bg-primary">{{ problems.length }} 题</span>
            </div>
          </div>
          <div class="card-body">
            <div v-if="problems.length > 0">
              <div class="problem-list">
                <div 
                  v-for="(problem, index) in problems" 
                  :key="problem.id" 
                  class="card problem-card mb-3"
                >
                  <div class="card-body">
                    <div class="problem-actions">
                      <div class="btn-group btn-group-sm">
                        <button 
                          class="btn btn-outline-primary" 
                          title="编辑题目"
                          @click="editProblem(problem.id)"
                        >
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button 
                          type="button" 
                          class="btn btn-outline-danger" 
                          title="删除题目"
                          @click="deleteProblem(problem.id)"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                    
                    <h5 class="card-title">第 {{ problem.order || index + 1 }} 题</h5>
                    <div class="markdown-content" v-html="renderMarkdown(problem.problem_text)"></div>
                    
                    <div v-if="problem.reference_answer" class="mt-3">
                      <button 
                        class="btn btn-sm btn-outline-info" 
                        type="button" 
                        @click="toggleAnswer(problem.id)"
                      >
                        {{ showAnswers[problem.id] ? '隐藏参考答案' : '显示参考答案' }}
                      </button>
                      <div v-show="showAnswers[problem.id]" class="mt-2">
                        <div class="card card-body bg-light">
                          <div class="markdown-content" v-html="renderMarkdown(problem.reference_answer)"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-5">
              <i class="bi bi-inbox display-4 mb-3 text-muted"></i>
              <p class="text-muted">暂无题目，请使用左侧面板添加题目</p>
              <button 
                class="btn btn-primary mt-2"
                @click="showAddProblemModal = true"
              >
                <i class="bi bi-plus-circle me-1"></i>添加第一个题目
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 手动添加题目模态框 -->
    <div v-if="showAddProblemModal" class="modal fade show" style="display: block;" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">添加题目</h5>
            <button 
              type="button" 
              class="btn-close" 
              @click="showAddProblemModal = false"
            ></button>
          </div>
          <div class="modal-body">
            <form id="addProblemForm" @submit.prevent="addProblem">
              <div class="mb-3">
                <label for="problem_text" class="form-label">题目内容</label>
                <textarea 
                  class="form-control" 
                  id="problem_text" 
                  v-model="problemForm.problem_text"
                  rows="5" 
                  required
                  placeholder="请输入题目内容，支持Markdown格式"
                ></textarea>
                <div class="form-text">支持Markdown格式</div>
              </div>
              
              <div class="mb-3">
                <label for="reference_answer" class="form-label">参考答案</label>
                <textarea 
                  class="form-control" 
                  id="reference_answer" 
                  v-model="problemForm.reference_answer"
                  rows="3"
                  placeholder="输入参考答案（可选）"
                ></textarea>
              </div>
              
              <div class="mb-3">
                <label for="grading_criteria" class="form-label">评分标准</label>
                <textarea 
                  class="form-control" 
                  id="grading_criteria" 
                  v-model="problemForm.grading_criteria"
                  rows="3"
                  placeholder="描述如何评分，AI批改系统将参考这些标准"
                ></textarea>
                <div class="form-text">描述如何评分，AI批改系统将参考这些标准</div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button 
              type="button" 
              class="btn btn-secondary"
              @click="showAddProblemModal = false"
            >
              取消
            </button>
            <button 
              type="button" 
              class="btn btn-primary"
              @click="addProblem"
              :disabled="isAddingProblem"
            >
              {{ isAddingProblem ? '添加中...' : '添加题目' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showAddProblemModal" class="modal-backdrop fade show"></div>

    <!-- 智能生成题目模态框 -->
    <div v-if="showGenerateProblemModal" class="modal fade show" style="display: block;" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">智能生成题目</h5>
            <button 
              type="button" 
              class="btn-close" 
              @click="showGenerateProblemModal = false"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="generateProblem">
              <div class="row">
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="subject" class="form-label">学科领域</label>
                    <select class="form-select" v-model="generateForm.subject">
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
                    <select class="form-select" v-model="generateForm.difficulty">
                      <option value="简单">简单</option>
                      <option value="中等">中等</option>
                      <option value="困难">困难</option>
                    </select>
                  </div>
                  
                  <div class="mb-3">
                    <label for="pattern_type" class="form-label">生成模式</label>
                    <select class="form-select" v-model="generateForm.pattern_type">
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
                      <input type="number" class="form-control" v-model="generateForm.choice" min="0">
                    </div>
                    <div class="input-group mb-2">
                      <span class="input-group-text">判断题</span>
                      <input type="number" class="form-control" v-model="generateForm.true_false" min="0">
                    </div>
                    <div class="input-group mb-2">
                      <span class="input-group-text">填空题</span>
                      <input type="number" class="form-control" v-model="generateForm.gap_filling" min="0">
                    </div>
                    <div class="input-group mb-2">
                      <span class="input-group-text">编程题</span>
                      <input type="number" class="form-control" v-model="generateForm.programming" min="0">
                    </div>
                    <div class="form-text">输入0表示不生成该类型题目</div>
                  </div>
                  
                  <div class="mb-3">
                    <label for="file" class="form-label">上传题库（可选）</label>
                    <input 
                      type="file" 
                      class="form-control" 
                      ref="fileInput"
                      @change="handleFileChange"
                      accept=".txt,.doc,.docx"
                    >
                    <div class="form-text">上传题库文件，AI将从中抽取相关题目</div>
                    
                    <!-- 文件选择状态提示 -->
                    <div v-if="selectedFile" class="mt-2">
                      <div class="alert alert-success d-flex justify-content-between align-items-center py-2">
                        <span>
                          <i class="bi bi-file-earmark-text me-1"></i>
                          {{ selectedFile.name }} ({{ (selectedFile.size / 1024).toFixed(2) }} KB)
                        </span>
                        <button 
                          type="button" 
                          class="btn btn-sm btn-outline-danger"
                          @click="clearFile"
                          title="移除文件"
                        >
                          <i class="bi bi-x"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="alert alert-info">
                <i class="bi bi-info-circle me-1"></i>建议每种题型数量不超过5个，以保证生成质量。
              </div>
              
              <!-- 生成结果预览 -->
              <div v-if="generatedProblemText" class="card mt-3">
                <div class="card-header">生成的题目预览</div>
                <div class="card-body">
                  <div class="markdown-content" v-html="renderMarkdown(generatedProblemText)"></div>
                </div>
              </div>
              
              <!-- 错误信息 -->
              <div v-if="generationError" class="alert alert-danger mt-3">
                <i class="bi bi-exclamation-triangle me-1"></i>
                {{ generationError }}
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <!-- 加载状态 -->
            <div v-if="isGenerating" class="spinner-border text-primary me-2" role="status">
              <span class="visually-hidden">生成中...</span>
            </div>
            
            <button 
              type="button" 
              class="btn btn-outline-secondary"
              @click="closeGenerateModal"
            >
              取消
            </button>
            
            <!-- 生成按钮 -->
            <button 
              v-if="!generatedProblemText"
              type="button" 
              class="btn btn-primary"
              @click="generateProblem"
              :disabled="isGenerating"
            >
              {{ isGenerating ? '生成中...' : '生成题目' }}
            </button>
            
            <!-- 保存和打印按钮 -->
            <template v-if="generatedProblemText">
              <button 
                type="button" 
                class="btn btn-success"
                @click="saveGeneratedProblem"
                :disabled="isSavingGenerated"
              >
                {{ isSavingGenerated ? '保存中...' : '保存题目' }}
              </button>
              <button 
                type="button" 
                class="btn btn-outline-info"
                @click="printGeneratedProblem"
              >
                <i class="bi bi-printer me-1"></i>打印
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showGenerateProblemModal" class="modal-backdrop fade show"></div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
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
    return '' // 使用外部默认转义
  }
})

export default {
  name: 'EditAssignment',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const assignmentId = route.params.id
    
    const assignment = ref(null)
    const problems = ref([])
    const isLoading = ref(true)
    const isSaving = ref(false)
    const isAddingProblem = ref(false)
    const showAddProblemModal = ref(false)
    const showGenerateProblemModal = ref(false)
    const showAnswers = ref({})
    const selectedFile = ref(null)
    const fileInput = ref(null)

    const formData = reactive({
      title: '',
      description: '',
      due_date: ''
    })

    const problemForm = reactive({
      problem_text: '',
      reference_answer: '',
      grading_criteria: ''
    })

    const generateForm = reactive({
      subject: '计算机',
      difficulty: '中等',
      pattern_type: '从上传题库中抽取',
      choice: 1,
      true_false: 1,
      gap_filling: 1,
      programming: 1
    })

    const generatedProblemText = ref('')
    const generationError = ref('')
    const isGenerating = ref(false)
    const isSavingGenerated = ref(false)

    const loadAssignment = async () => {
      try {
        const response = await teacherAPI.getAssignment(assignmentId)
        if (response.data.success) {
          assignment.value = response.data.assignment
          problems.value = response.data.assignment.problems || []
          
          // 填充表单数据
          formData.title = assignment.value.title
          formData.description = assignment.value.description || ''
          formData.due_date = assignment.value.due_date ? 
            new Date(assignment.value.due_date).toISOString().split('T')[0] : ''
        } else {
          throw new Error(response.data.message || '加载作业失败')
        }
      } catch (error) {
        console.error('加载作业失败:', error)
        alert('加载作业失败')
        router.push('/teacher/courses')
      } finally {
        isLoading.value = false
      }
    }

    const updateAssignment = async () => {
      isSaving.value = true
      try {
        const response = await teacherAPI.updateAssignment(assignmentId, {
          title: formData.title,
          description: formData.description || null,
          due_date: formData.due_date || null
        })
        
        if (response.data.success) {
          assignment.value = { ...assignment.value, ...formData }
          alert('作业信息保存成功')
        } else {
          throw new Error(response.data.message || '保存失败')
        }
      } catch (error) {
        console.error('保存作业失败:', error)
        alert('保存作业失败')
      } finally {
        isSaving.value = false
      }
    }

    const addProblem = async () => {
      if (!problemForm.problem_text.trim()) {
        alert('请输入题目内容')
        return
      }

      isAddingProblem.value = true
      try {
        const response = await teacherAPI.addProblem(assignmentId, {
          problem_text: problemForm.problem_text.trim(),
          reference_answer: problemForm.reference_answer.trim() || null,
          grading_criteria: problemForm.grading_criteria.trim() || null,
          order: problems.value.length + 1
        })
        
        if (response.data.success) {
          problems.value.push(response.data.problem)
          
          // 清空表单
          problemForm.problem_text = ''
          problemForm.reference_answer = ''
          problemForm.grading_criteria = ''
          
          showAddProblemModal.value = false
          alert('题目添加成功')
        } else {
          throw new Error(response.data.message || '添加题目失败')
        }
      } catch (error) {
        console.error('添加题目失败:', error)
        alert('添加题目失败')
      } finally {
        isAddingProblem.value = false
      }
    }

    const editProblem = (problemId) => {
      router.push(`/teacher/problems/${problemId}/edit`)
    }

    const deleteProblem = async (problemId) => {
      if (!confirm('确定要删除这个题目吗？')) return
      
      try {
        const response = await teacherAPI.deleteProblem(problemId)
        if (response.data.success) {
          problems.value = problems.value.filter(p => p.id !== problemId)
          alert('题目删除成功')
        } else {
          throw new Error(response.data.message || '删除失败')
        }
      } catch (error) {
        console.error('删除题目失败:', error)
        alert('删除题目失败')
      }
    }

    const toggleAnswer = (problemId) => {
      showAnswers.value[problemId] = !showAnswers.value[problemId]
    }

    const renderMarkdown = (text) => {
      if (!text) return ''
      
      try {
        // 使用markdown-it进行渲染
        let html = md.render(text)
        
        // 处理外部链接，添加target="_blank"
        html = html.replace(/<a href="http/g, '<a target="_blank" rel="noopener noreferrer" href="http')
        
        return html
      } catch (error) {
        console.error('Markdown渲染错误:', error)
        // 如果渲染失败，返回纯文本
        return text.replace(/\n/g, '<br>')
      }
    }

    const generateProblem = async () => {
      // 验证题目数量
      const total = parseInt(generateForm.choice) + parseInt(generateForm.true_false) + 
                   parseInt(generateForm.gap_filling) + parseInt(generateForm.programming)
      
      if (total <= 0) {
        alert('请至少选择一种题型并输入数量')
        return
      }

      isGenerating.value = true
      generationError.value = ''
      
      try {
        let response
        
        // 如果有文件上传，使用FormData
        if (selectedFile.value) {
          const uploadData = new FormData()
          uploadData.append('assignment_id', assignmentId)
          uploadData.append('subject', generateForm.subject)
          uploadData.append('difficulty', generateForm.difficulty)
          uploadData.append('pattern_type', generateForm.pattern_type)
          uploadData.append('choice', generateForm.choice)
          uploadData.append('true_false', generateForm.true_false)
          uploadData.append('gap_filling', generateForm.gap_filling)
          uploadData.append('programming', generateForm.programming)
          uploadData.append('file', selectedFile.value)
          
          response = await teacherAPI.generateProblemWithFile(uploadData)
        } else {
          // 没有文件，使用原来的方法
          response = await teacherAPI.generateProblem(assignmentId, generateForm)
        }
        
        if (response.data.success) {
          generatedProblemText.value = response.data.problem.problem_text
        } else {
          throw new Error(response.data.message || '生成失败')
        }
      } catch (error) {
        console.error('生成题目失败:', error)
        generationError.value = error.response?.data?.message || error.message || '生成失败'
      } finally {
        isGenerating.value = false
      }
    }

    const saveGeneratedProblem = async () => {
      if (!generatedProblemText.value.trim()) {
        alert('没有可保存的题目')
        return
      }

      isSavingGenerated.value = true
      try {
        const response = await teacherAPI.addProblem(assignmentId, {
          problem_text: generatedProblemText.value.trim(),
          reference_answer: '',
          grading_criteria: '',
          order: problems.value.length + 1
        })
        
        if (response.data.success) {
          problems.value.push(response.data.problem)
          closeGenerateModal()
          alert('题目保存成功')
        } else {
          throw new Error(response.data.message || '保存失败')
        }
      } catch (error) {
        console.error('保存题目失败:', error)
        alert(error.response?.data?.message || '保存题目失败')
      } finally {
        isSavingGenerated.value = false
      }
    }

    const printGeneratedProblem = () => {
      if (!generatedProblemText.value) {
        alert('没有可打印的题目')
        return
      }
      
      const printWindow = window.open('', '_blank')
      printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>智能生成题目</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1 { font-size: 1.8rem; }
            h2 { font-size: 1.5rem; margin-top: 20px; }
            .problem { margin-bottom: 20px; }
          </style>
        </head>
        <body>
          <h1>智能生成题目</h1>
          <div class="problem">${renderMarkdown(generatedProblemText.value)}</div>
        </body>
        </html>
      `)
      
      printWindow.document.close()
      printWindow.focus()
      setTimeout(() => {
        printWindow.print()
      }, 500)
    }

    const closeGenerateModal = () => {
      showGenerateProblemModal.value = false
      generatedProblemText.value = ''
      generationError.value = ''
      selectedFile.value = null
      
      // 清除文件输入框
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }

    const handleFileChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        selectedFile.value = file
        console.log('选择文件:', file.name, '大小:', file.size, '类型:', file.type)
      } else {
        selectedFile.value = null
      }
    }

    const clearFile = () => {
      selectedFile.value = null
      // 清除文件输入框
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }

    onMounted(() => {
      loadAssignment()
    })

    return {
      assignment,
      problems,
      formData,
      problemForm,
      generateForm,
      isLoading,
      isSaving,
      isAddingProblem,
      showAddProblemModal,
      showGenerateProblemModal,
      showAnswers,
      generatedProblemText,
      generationError,
      isGenerating,
      isSavingGenerated,
      selectedFile,
      fileInput,
      updateAssignment,
      addProblem,
      editProblem,
      deleteProblem,
      toggleAnswer,
      renderMarkdown,
      generateProblem,
      saveGeneratedProblem,
      printGeneratedProblem,
      closeGenerateModal,
      handleFileChange,
      clearFile
    }
  }
}
</script>

<style scoped>
/* 全局容器样式 */
.edit-assignment {
  max-width: 1600px;
  margin: 0 auto;
  padding: 1.5rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: #f8fafc;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  margin-bottom: 2rem;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border-left: 4px solid #3b82f6;
}

.page-header h1 {
  color: #1f2937;
  font-weight: 700;
  font-size: 2.25rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-header p {
  color: #6b7280;
  margin-bottom: 0;
  font-size: 1.125rem;
}

/* 主要布局 */
.row {
  margin: 0 -0.75rem;
}

.col-md-4,
.col-md-8 {
  padding: 0 0.75rem;
}

/* 卡片样式 */
.card {
  border: none;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
}

.card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.card-header {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
  font-weight: 600;
  padding: 1.5rem;
  color: #1f2937;
  font-size: 1.125rem;
}

.card-body {
  padding: 1.5rem;
}

/* 表单样式 */
.form-label {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.form-control,
.form-select {
  border-radius: 10px;
  border: 2px solid #e5e7eb;
  padding: 0.875rem 1rem;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background: white;
}

.form-control:focus,
.form-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  outline: none;
}

.form-text {
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

/* 题目卡片 */
.problem-card {
  border-left: 4px solid #3b82f6;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.problem-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
  border-left-color: #2563eb;
}

.problem-actions {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 10;
}

.problem-actions .btn-group {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

/* Markdown内容样式 - 确保左对齐 */
:deep(.markdown-content),
:deep(.markdown-preview) {
  text-align: left !important;
  line-height: 1.7;
  color: #374151;
}

:deep(.markdown-content *),
:deep(.markdown-preview *) {
  text-align: left !important;
}

/* 标题样式 */
:deep(.markdown-content h1),
:deep(.markdown-content h2),
:deep(.markdown-content h3),
:deep(.markdown-content h4),
:deep(.markdown-content h5),
:deep(.markdown-content h6),
:deep(.markdown-preview h1),
:deep(.markdown-preview h2),
:deep(.markdown-preview h3),
:deep(.markdown-preview h4),
:deep(.markdown-preview h5),
:deep(.markdown-preview h6) {
  color: #1f2937;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
  text-align: left !important;
}

:deep(.markdown-content h1),
:deep(.markdown-preview h1) {
  font-size: 1.875rem;
  border-bottom: 3px solid #3b82f6;
  padding-bottom: 0.75rem;
}

:deep(.markdown-content h2),
:deep(.markdown-preview h2) {
  font-size: 1.5rem;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

:deep(.markdown-content h3),
:deep(.markdown-preview h3) {
  font-size: 1.25rem;
}

/* 段落样式 */
:deep(.markdown-content p),
:deep(.markdown-preview p) {
  margin-bottom: 1.25rem;
  line-height: 1.7;
  text-align: left !important;
}

/* 列表样式 */
:deep(.markdown-content ul),
:deep(.markdown-content ol),
:deep(.markdown-preview ul),
:deep(.markdown-preview ol) {
  margin-bottom: 1.25rem;
  padding-left: 2rem;
  text-align: left !important;
}

:deep(.markdown-content li),
:deep(.markdown-preview li) {
  margin-bottom: 0.5rem;
  text-align: left !important;
}

/* 代码样式 */
:deep(.markdown-content code),
:deep(.markdown-preview code) {
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', monospace;
  font-size: 0.875rem;
  color: #1e40af;
  border: 1px solid #cbd5e1;
}

:deep(.markdown-content pre),
:deep(.markdown-preview pre) {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  overflow-x: auto;
  margin-bottom: 1.5rem;
  text-align: left !important;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
}

:deep(.markdown-content pre code),
:deep(.markdown-preview pre code) {
  background-color: transparent;
  padding: 0;
  color: inherit;
  font-size: 0.875rem;
  border: none;
}

/* 引用样式 */
:deep(.markdown-content blockquote),
:deep(.markdown-preview blockquote) {
  border-left: 4px solid #3b82f6;
  padding-left: 1.5rem;
  margin: 1.5rem 0;
  color: #4b5563;
  font-style: italic;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  padding: 1.5rem;
  border-radius: 12px;
  text-align: left !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* 表格样式 */
:deep(.markdown-content table),
:deep(.markdown-preview table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

:deep(.markdown-content th),
:deep(.markdown-content td),
:deep(.markdown-preview th),
:deep(.markdown-preview td) {
  border: 1px solid #e5e7eb;
  padding: 0.875rem;
  text-align: left !important;
}

:deep(.markdown-content th),
:deep(.markdown-preview th) {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  font-weight: 600;
  text-align: left !important;
  color: #1f2937;
}

:deep(.markdown-content tr:nth-child(even)),
:deep(.markdown-preview tr:nth-child(even)) {
  background-color: #f9fafb;
}

/* 链接样式 */
:deep(.markdown-content a),
:deep(.markdown-preview a) {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

:deep(.markdown-content a:hover),
:deep(.markdown-preview a:hover) {
  color: #1e40af;
  text-decoration: underline;
}

/* 分隔线样式 */
:deep(.markdown-content hr),
:deep(.markdown-preview hr) {
  border: none;
  border-top: 3px solid #e5e7eb;
  margin: 2rem 0;
  border-radius: 2px;
}

/* 强调样式 */
:deep(.markdown-content strong),
:deep(.markdown-content b),
:deep(.markdown-preview strong),
:deep(.markdown-preview b) {
  font-weight: 700;
  color: #1f2937;
}

:deep(.markdown-content em),
:deep(.markdown-content i),
:deep(.markdown-preview em),
:deep(.markdown-preview i) {
  font-style: italic;
  color: #4b5563;
}

/* 代码高亮优化 */
:deep(.markdown-content .hljs),
:deep(.markdown-preview .hljs) {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9) !important;
  text-align: left !important;
  border-radius: 8px;
}

/* 按钮样式 */
.btn {
  border-radius: 10px;
  font-weight: 600;
  padding: 0.75rem 1.25rem;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.39);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5);
  color: white;
}

.btn-outline-primary {
  background: white;
  color: #3b82f6;
  border: 2px solid #3b82f6;
}

.btn-outline-primary:hover {
  background: #3b82f6;
  color: white;
  transform: translateY(-1px);
}

.btn-outline-secondary {
  background: white;
  color: #6b7280;
  border: 2px solid #d1d5db;
}

.btn-outline-secondary:hover {
  background: #f3f4f6;
  color: #374151;
  border-color: #9ca3af;
}

.btn-outline-danger {
  background: white;
  color: #dc2626;
  border: 2px solid #dc2626;
}

.btn-outline-danger:hover {
  background: #dc2626;
  color: white;
  transform: translateY(-1px);
}

.btn-outline-info {
  background: white;
  color: #0ea5e9;
  border: 2px solid #0ea5e9;
}

.btn-outline-info:hover {
  background: #0ea5e9;
  color: white;
  transform: translateY(-1px);
}

.btn-success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.btn-success:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-1px);
  color: white;
}

/* 模态框样式 */
.modal {
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
}

.modal-content {
  border: none;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-header {
  border-bottom: 1px solid #e5e7eb;
  padding: 1.5rem;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  border-top: 1px solid #e5e7eb;
  padding: 1.5rem;
}

/* 统计卡片样式 */
.stat-item {
  padding: 1rem;
  text-align: center;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: #3b82f6;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

/* 文件选择样式 */
.alert-success {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  border: 2px solid #10b981;
  color: #047857;
  border-radius: 12px;
}

/* 加载状态 */
.loading-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  background: white;
  border-radius: 16px;
  margin: 2rem 0;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .edit-assignment {
    max-width: 1200px;
    padding: 1.25rem;
  }
}

@media (max-width: 1024px) {
  .edit-assignment {
    padding: 1rem;
  }
  
  .page-header {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .card-body {
    padding: 1.25rem;
  }
}

@media (max-width: 768px) {
  .edit-assignment {
    padding: 0.75rem;
  }
  
  .col-md-4,
  .col-md-8 {
    padding: 0 0.375rem;
  }
  
  .row {
    margin: 0 -0.375rem;
  }
  
  .problem-actions {
    position: static;
    margin-bottom: 1rem;
    text-align: right;
  }
  
  .d-flex.justify-content-between {
    flex-direction: column;
    gap: 1rem;
  }
  
  .page-header {
    padding: 1.25rem;
  }
  
  .page-header h1 {
    font-size: 1.75rem;
  }
  
  .card-body {
    padding: 1rem;
  }
}

@media (max-width: 576px) {
  .edit-assignment {
    padding: 0.5rem;
  }
  
  .page-header {
    padding: 1rem;
    margin-bottom: 1rem;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .card-body {
    padding: 0.875rem;
  }
  
  .btn {
    padding: 0.625rem 1rem;
    font-size: 0.875rem;
  }
  
  .modal-body,
  .modal-header,
  .modal-footer {
    padding: 1rem;
  }
}
</style>
