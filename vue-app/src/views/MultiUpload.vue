<template>
  <div class="multi-upload">
    <div class="page-header">
      <h1><i class="bi bi-files me-2"></i>试卷自动评分系统</h1>
      <p>上传答案文件和评分标准，系统将自动分析并给出评分结果</p>
    </div>
    
    <form @submit.prevent="submitFiles">
      <div class="form-section">
        <h4><i class="bi bi-upload me-2"></i>文件上传</h4>
        <p class="text-muted mb-4">请依次上传三个TXT格式文件，系统将自动进行处理</p>
        
        <div class="row">
          <div class="col-md-4 file-container">
            <div class="file-upload-wrapper">
              <div class="mb-2"><i class="bi bi-file-earmark-text fs-2 text-primary"></i></div>
              <label for="file1" class="form-label">学生答案</label>
              <input 
                type="file" 
                class="form-control file-input" 
                id="file1" 
                @change="handleFileChange($event, 'file1')"
                accept=".txt" 
                required
              >
              <div class="file-upload-message">{{ fileMessages.file1 || '支持 .txt 格式' }}</div>
              <div v-show="fileStatuses.file1" class="file-status" :class="fileStatusClasses.file1">
                <i :class="fileStatusIcons.file1"></i> {{ fileStatusTexts.file1 }}
              </div>
            </div>
          </div>
          
          <div class="col-md-4 file-container">
            <div class="file-upload-wrapper">
              <div class="mb-2"><i class="bi bi-file-earmark-text fs-2 text-primary"></i></div>
              <label for="file2" class="form-label">标准题目</label>
              <input 
                type="file" 
                class="form-control file-input" 
                id="file2" 
                @change="handleFileChange($event, 'file2')"
                accept=".txt" 
                required
              >
              <div class="file-upload-message">{{ fileMessages.file2 || '支持 .txt 格式' }}</div>
              <div v-show="fileStatuses.file2" class="file-status" :class="fileStatusClasses.file2">
                <i :class="fileStatusIcons.file2"></i> {{ fileStatusTexts.file2 }}
              </div>
            </div>
          </div>
          
          <div class="col-md-4 file-container">
            <div class="file-upload-wrapper">
              <div class="mb-2"><i class="bi bi-file-earmark-text fs-2 text-primary"></i></div>
              <label for="file3" class="form-label">评分标准</label>
              <input 
                type="file" 
                class="form-control file-input" 
                id="file3" 
                @change="handleFileChange($event, 'file3')"
                accept=".txt" 
                required
              >
              <div class="file-upload-message">{{ fileMessages.file3 || '支持 .txt 格式' }}</div>
              <div v-show="fileStatuses.file3" class="file-status" :class="fileStatusClasses.file3">
                <i :class="fileStatusIcons.file3"></i> {{ fileStatusTexts.file3 }}
              </div>
            </div>
          </div>
        </div>
        
        <div class="alert alert-info mt-4">
          <i class="bi bi-info-circle-fill me-2"></i>
          <strong>操作说明：</strong> 请上传三个文件 - 学生答案文件、标准题目文件和评分标准文件。系统将自动进行答案评估和评分。
        </div>
      </div>
      
      <div class="d-grid gap-2 col-6 mx-auto mt-4">
        <button type="submit" class="btn btn-primary btn-lg" :disabled="isProcessing">
          <span v-if="isProcessing" class="spinner-border spinner-border-sm me-2"></span>
          <i v-else class="bi bi-lightning-charge"></i>
          {{ isProcessing ? '评分中...' : '开始评分' }}
        </button>
      </div>
    </form>
    
    <!-- 加载提示 -->
    <div v-if="isProcessing" class="spinner-container">
      <div class="d-flex flex-column align-items-center">
        <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;">
          <span class="visually-hidden">正在处理...</span>
        </div>
        <p class="fs-5">正在处理文件，请稍候...</p>
        <p class="text-muted small">处理多个文件可能需要较长时间</p>
      </div>
    </div>
    
    <!-- 结果显示 -->
    <div v-if="showResult" class="result-container">
      <div class="result-header">
        <h4><i class="bi bi-award"></i> 评分结果</h4>
        <div>
          <button class="btn btn-sm btn-outline-secondary" @click="toggleRawJson">
            <i class="bi bi-code-slash"></i> {{ showRawJson ? '显示处理结果' : '显示原始JSON' }}
          </button>
          <button class="btn btn-sm btn-outline-secondary" @click="copyResult">
            <i class="bi bi-clipboard"></i> 复制结果
          </button>
          <button class="btn btn-sm btn-outline-primary" @click="downloadResult">
            <i class="bi bi-file-earmark-pdf"></i> 导出PDF
          </button>
        </div>
      </div>
      
      <div v-if="showRawJson" class="result-content">
        <pre>{{ rawJsonResult }}</pre>
      </div>
      <div v-else class="result-content" v-html="processedResult"></div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { workflowAPI } from '../utils/api'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css' // 导入代码高亮样式，可选择其他样式

export default {
  name: 'MultiUpload',
  setup() {
    const isProcessing = ref(false)
    const showResult = ref(false)
    const showRawJson = ref(false)
    const rawJsonResult = ref('')
    const processedResult = ref('')
    
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
    
    const files = reactive({
      file1: null,
      file2: null,
      file3: null
    })
    
    const fileMessages = reactive({
      file1: '',
      file2: '',
      file3: ''
    })
    
    const fileStatuses = reactive({
      file1: false,
      file2: false,
      file3: false
    })
    
    const fileStatusClasses = computed(() => ({
      file1: files.file1 && files.file1.name.toLowerCase().endsWith('.txt') ? 'text-success' : 'text-danger',
      file2: files.file2 && files.file2.name.toLowerCase().endsWith('.txt') ? 'text-success' : 'text-danger',
      file3: files.file3 && files.file3.name.toLowerCase().endsWith('.txt') ? 'text-success' : 'text-danger'
    }))
    
    const fileStatusIcons = computed(() => ({
      file1: files.file1 && files.file1.name.toLowerCase().endsWith('.txt') ? 'bi bi-check-circle' : 'bi bi-exclamation-triangle',
      file2: files.file2 && files.file2.name.toLowerCase().endsWith('.txt') ? 'bi bi-check-circle' : 'bi bi-exclamation-triangle',
      file3: files.file3 && files.file3.name.toLowerCase().endsWith('.txt') ? 'bi bi-check-circle' : 'bi bi-exclamation-triangle'
    }))
    
    const fileStatusTexts = computed(() => ({
      file1: files.file1 && files.file1.name.toLowerCase().endsWith('.txt') ? '已选择' : '请上传TXT文件',
      file2: files.file2 && files.file2.name.toLowerCase().endsWith('.txt') ? '已选择' : '请上传TXT文件',
      file3: files.file3 && files.file3.name.toLowerCase().endsWith('.txt') ? '已选择' : '请上传TXT文件'
    }))

    const handleFileChange = (event, fileKey) => {
      const file = event.target.files[0]
      if (file) {
        files[fileKey] = file
        fileMessages[fileKey] = file.name
        fileStatuses[fileKey] = true
      } else {
        files[fileKey] = null
        fileMessages[fileKey] = ''
        fileStatuses[fileKey] = false
      }
    }

    const submitFiles = async () => {
      // 验证所有文件都已上传且为txt格式
      const allFilesValid = Object.values(files).every(file => 
        file && file.name.toLowerCase().endsWith('.txt')
      )
      
      if (!allFilesValid) {
        alert('请确保所有文件都已上传且为TXT格式')
        return
      }

      isProcessing.value = true
      showResult.value = false

      try {
        const formData = new FormData()
        formData.append('file1', files.file1)
        formData.append('file2', files.file2)
        formData.append('file3', files.file3)

        const response = await workflowAPI.runMultiWorkflow(formData)

        // 保存原始JSON结果
        rawJsonResult.value = JSON.stringify(response.data, null, 2)
        
        // 处理结果内容
        if (response.data?.data?.outputs?.output) {
          const output = response.data.data.outputs.output
          // 使用 markdown-it 渲染 Markdown
          processedResult.value = md.render(output)
          enhanceResultContent()
        } else {
          processedResult.value = `
            <div class="alert alert-info">无法获取评分结果或返回格式不符合预期。</div>
            <div class="text-muted small mt-2">您可以点击"显示原始JSON"查看完整返回数据。</div>
          `
        }
        
        showResult.value = true
      } catch (error) {
        console.error('评分失败:', error)
        rawJsonResult.value = `发生错误: ${error.message}`
        processedResult.value = `<div class="alert alert-danger">评分失败: ${error.response?.data?.message || error.message}</div>`
        showResult.value = true
      } finally {
        isProcessing.value = false
      }
    }

    // 增强结果内容展示效果
    const enhanceResultContent = () => {
      // 这里可以添加更多的格式化逻辑
      // 例如添加样式或进行后处理
      
      // 添加表格样式
      const tableStyles = `
        <style>
          .result-content table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            text-align: left;
          }
          .result-content table * {
            text-align: left;
          }
          .result-content th, .result-content td {
            border: 1px solid #e1e1e1;
            padding: 8px 12px;
            text-align: left;
          }
          .result-content th {
            background-color: #f5f5f5;
            font-weight: 600;
            text-align: left;
          }
          .result-content tr {
            text-align: left;
          }
          .result-content tr:nth-child(even) {
            background-color: #f9f9f9;
          }
        </style>
      `
      
      processedResult.value = tableStyles + processedResult.value
    }

    const toggleRawJson = () => {
      showRawJson.value = !showRawJson.value
    }

    const copyResult = async () => {
      try {
        const textToCopy = showRawJson.value ? rawJsonResult.value : 
          document.querySelector('.result-content').innerText
        await navigator.clipboard.writeText(textToCopy)
        alert('结果已复制到剪贴板')
      } catch (error) {
        console.error('复制失败:', error)
        alert('复制失败，请手动选择并复制')
      }
    }

    const downloadResult = () => {
      if (showRawJson.value) {
        // 下载JSON文件
        const blob = new Blob([rawJsonResult.value], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = '评分结果.json'
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
      } else {
        // 导出PDF（这里可以集成html2pdf等库）
        alert('PDF导出功能开发中...')
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
      isProcessing,
      showResult,
      showRawJson,
      rawJsonResult,
      processedResult,
      files,
      fileMessages,
      fileStatuses,
      fileStatusClasses,
      fileStatusIcons,
      fileStatusTexts,
      handleFileChange,
      submitFiles,
      toggleRawJson,
      copyResult,
      downloadResult
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

.form-section {
  background-color: #f7fbff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  border-left: 4px solid #3c6e71;
}

.form-section h4 {
  color: #3c6e71;
  margin-bottom: 15px;
  font-weight: 600;
}

.file-upload-wrapper {
  position: relative;
  margin-bottom: 15px;
  border: 2px dashed #3c6e71;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  transition: all 0.3s;
}

.file-upload-wrapper:hover {
  background-color: #f0f7f7;
}

.file-upload-message {
  font-size: 1rem;
  color: #6c757d;
  margin: 10px 0;
}

.file-status {
  margin-top: 5px;
}

.file-container {
  margin-bottom: 20px;
}

.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  margin-top: 30px;
}

.result-container {
  margin-top: 30px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  background-color: #f8f9fa;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #dee2e6;
}

.result-content {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  text-align: left;
}

/* 允许渲染 Markdown 内容的样式 */
:deep(.result-content) {
  line-height: 1.6;
  text-align: left;
}

:deep(.result-content *) {
  text-align: left;
}

:deep(.result-content h1) {
  font-size: 24px;
  margin: 20px 0 15px;
  color: #3c6e71;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 8px;
  text-align: left;
}

:deep(.result-content h2) {
  font-size: 20px;
  margin: 20px 0 12px;
  color: #2c3e50;
  padding-bottom: 5px;
  border-bottom: 1px solid #f0f0f0;
  text-align: left;
}

:deep(.result-content h3) {
  font-size: 18px;
  margin: 16px 0 10px;
  color: #2c3e50;
  text-align: left;
}

:deep(.result-content ul),
:deep(.result-content ol) {
  padding-left: 25px;
  margin: 10px 0;
  text-align: left;
}

:deep(.result-content li) {
  margin-bottom: 5px;
  text-align: left;
}

:deep(.result-content p) {
  margin: 10px 0;
  text-align: left;
}

:deep(.result-content a) {
  color: #3c6e71;
  text-decoration: none;
}

:deep(.result-content a:hover) {
  text-decoration: underline;
}

:deep(.result-content blockquote) {
  border-left: 4px solid #e0e0e0;
  padding: 10px 15px;
  margin: 15px 0;
  background-color: #f8f9fa;
  color: #666;
  text-align: left;
}

:deep(.result-content code:not(.hljs)) {
  background-color: #f5f5f5;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9em;
}

:deep(.result-content pre) {
  background-color: #f8f9fa;
  border-radius: 6px;
  margin: 15px 0;
  overflow-x: auto;
  text-align: left;
}

:deep(.result-content .hljs) {
  padding: 15px;
  border-radius: 5px;
  font-family: 'Courier New', Courier, monospace;
}

:deep(.result-content strong) {
  color: #3c6e71;
  font-weight: 600;
}

:deep(.result-content em) {
  font-style: italic;
}

:deep(.result-content img) {
  max-width: 100%;
  border-radius: 5px;
  margin: 10px 0;
}

:deep(.result-content hr) {
  border: 0;
  border-top: 1px solid #eee;
  margin: 20px 0;
}

:deep(.score-highlight) {
  font-size: 18px;
  font-weight: bold;
  color: #e74c3c;
  padding: 5px 10px;
  background-color: #fef9f9;
  border-radius: 4px;
  border-left: 3px solid #e74c3c;
  display: inline-block;
  margin: 5px 0;
}

:deep(.error-list) {
  background-color: #fff8f8;
  border-left: 3px solid #e74c3c;
  padding: 10px 15px;
  margin: 15px 0;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .result-header {
    flex-direction: column;
    gap: 10px;
  }
  
  .result-header > div {
    display: flex;
    gap: 5px;
    flex-wrap: wrap;
  }
}
</style> 