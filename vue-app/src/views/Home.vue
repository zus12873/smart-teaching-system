<template>
  <div class="home-content">
    <div class="page-header">
      <h1><i class="bi bi-mortarboard-fill me-2"></i>智能教学系统</h1>
      <p>基于人工智能的智能教学辅助平台</p>
      <div class="mt-3">
        <router-link to="/api-test" class="btn btn-outline-secondary btn-sm">
          <i class="bi bi-gear me-1"></i>API测试
        </router-link>
      </div>
    </div>
    
    <!-- 功能卡片 -->
    <div class="row text-center">
      <div class="col-md-4 mb-4">
        <div class="card h-100 feature-card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0"><i class="bi bi-journals me-2"></i>智能出题</h5>
          </div>
          <div class="card-body">
            <p class="card-text">
              基于人工智能的题目生成系统，可以根据教学需求自动生成各种类型的题目，包括选择题、判断题、填空题和编程题。
            </p>
            <router-link to="/problem-generation" class="btn btn-primary">开始使用</router-link>
          </div>
        </div>
      </div>
      
      <div class="col-md-4 mb-4">
        <div class="card h-100 feature-card">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0"><i class="bi bi-check-circle me-2"></i>智能批改</h5>
          </div>
          <div class="card-body">
            <p class="card-text">
              智能批改系统，可以自动评阅学生提交的答案，提供详细的评分和反馈，大大减轻教师的工作负担。
            </p>
            <router-link to="/multi-upload" class="btn btn-success">开始使用</router-link>
          </div>
        </div>
      </div>
      
      <div class="col-md-4 mb-4">
        <div class="card h-100 feature-card">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0"><i class="bi bi-graph-up me-2"></i>学习分析</h5>
          </div>
          <div class="card-body">
            <p class="card-text">
              学习数据分析平台，可以对学生的学习情况进行全面分析，提供个性化学习建议和教学决策支持。
            </p>
            <button class="btn btn-info" disabled>即将推出</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 使用指南 -->
    <div class="mt-5">
      <div class="card">
        <div class="card-header bg-light">
          <h5 class="mb-0">使用指南</h5>
        </div>
        <div class="card-body">
          <div class="accordion" id="accordionGuide">
            <div class="accordion-item">
              <h2 class="accordion-header" id="headingOne">
                <button 
                  class="accordion-button" 
                  type="button" 
                  data-bs-toggle="collapse" 
                  data-bs-target="#collapseOne" 
                  aria-expanded="true" 
                  aria-controls="collapseOne"
                >
                  <i class="bi bi-journals me-2"></i>智能出题使用方法
                </button>
              </h2>
              <div 
                id="collapseOne" 
                class="accordion-collapse collapse show" 
                aria-labelledby="headingOne" 
                data-bs-parent="#accordionGuide"
              >
                <div class="accordion-body">
                  <ol class="text-start">
                    <li>选择或上传题库文件</li>
                    <li>设置生成题目的数量和类型</li>
                    <li>选择题目难度和科目</li>
                    <li>点击生成按钮，系统将自动生成题目</li>
                    <li>查看和下载生成的题目</li>
                  </ol>
                </div>
              </div>
            </div>
            <div class="accordion-item">
              <h2 class="accordion-header" id="headingTwo">
                <button 
                  class="accordion-button collapsed" 
                  type="button" 
                  data-bs-toggle="collapse" 
                  data-bs-target="#collapseTwo" 
                  aria-expanded="false" 
                  aria-controls="collapseTwo"
                >
                  <i class="bi bi-check-circle me-2"></i>智能批改使用方法
                </button>
              </h2>
              <div 
                id="collapseTwo" 
                class="accordion-collapse collapse" 
                aria-labelledby="headingTwo" 
                data-bs-parent="#accordionGuide"
              >
                <div class="accordion-body">
                  <ol class="text-start">
                    <li>上传学生答案文件</li>
                    <li>上传标准题目文件</li>
                    <li>上传评分标准文件</li>
                    <li>点击评分按钮，系统将自动评阅答案</li>
                    <li>查看评分结果和详细反馈</li>
                    <li>导出评分报告</li>
                  </ol>
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
export default {
  name: 'Home'
}
</script>

<style scoped>
.page-header {
  text-align: center;
  margin-bottom: 30px;
  border-bottom: 2px solid #1976d2;
  padding-bottom: 20px;
}

.page-header h1 {
  color: #1565c0;
  font-weight: 600;
}

.page-header p {
  color: #424242;
  font-size: 16px;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(33, 150, 243, 0.15);
}

.accordion-button {
  font-weight: 500;
}

.accordion-button:not(.collapsed) {
  background-color: #e3f2fd;
  color: #1976d2;
}
</style> 