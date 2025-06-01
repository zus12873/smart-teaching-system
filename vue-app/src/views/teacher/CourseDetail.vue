<template>
  <div class="course-detail">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h1 class="display-6 mb-1">
            <i class="bi bi-journal-album me-2 text-primary"></i>
            {{ course?.name || '课程详情' }}
          </h1>
          <p class="text-muted mb-0">{{ course?.description || '暂无课程描述' }}</p>
        </div>
        <router-link to="/teacher/courses" class="btn btn-outline-secondary">
          <i class="bi bi-arrow-left me-1"></i>返回课程列表
        </router-link>
      </div>
      
      <!-- 课程统计卡片 -->
      <div class="row g-3">
        <div class="col-md-4">
          <div class="stat-card">
            <div class="stat-icon bg-primary">
              <i class="bi bi-people-fill"></i>
            </div>
            <div class="stat-content">
              <h3>{{ students.length }}</h3>
              <p>选课学生</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat-card">
            <div class="stat-icon bg-success">
              <i class="bi bi-file-earmark-text-fill"></i>
            </div>
            <div class="stat-content">
              <h3>{{ assignments.length }}</h3>
              <p>课程作业</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat-card">
            <div class="stat-icon bg-info">
              <i class="bi bi-calendar3"></i>
            </div>
            <div class="stat-content">
              <h3>{{ formatDate(course?.created_at) }}</h3>
              <p>创建时间</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-area">
      <!-- 选项卡 -->
      <ul class="nav nav-pills mb-4" role="tablist">
        <li class="nav-item">
          <button 
            class="nav-link"
            :class="{ active: activeTab === 'assignments' }"
            @click="activeTab = 'assignments'"
          >
            <i class="bi bi-file-earmark-text me-2"></i>课程作业 ({{ assignments.length }})
          </button>
        </li>
        <li class="nav-item">
          <button 
            class="nav-link"
            :class="{ active: activeTab === 'students' }"
            @click="activeTab = 'students'"
          >
            <i class="bi bi-people me-2"></i>选课学生 ({{ students.length }})
          </button>
        </li>
      </ul>

      <!-- 作业列表 -->
      <div v-show="activeTab === 'assignments'" class="tab-content">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h3>课程作业</h3>
          <button class="btn btn-primary" @click="createAssignment">
            <i class="bi bi-plus-circle me-1"></i>创建新作业
          </button>
        </div>

        <div v-if="assignments.length > 0" class="table-container">
          <div class="table-responsive">
            <table class="table table-hover">
              <thead class="table-light">
                <tr>
                  <th>作业标题</th>
                  <th>描述</th>
                  <th>题目数量</th>
                  <th>提交数量</th>
                  <th>完成率</th>
                  <th>创建时间</th>
                  <th>截止时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="assignment in assignments" :key="assignment.id">
                  <td>
                    <div class="fw-semibold">{{ assignment.title }}</div>
                  </td>
                  <td>
                    <span class="text-muted">{{ assignment.description || '暂无描述' }}</span>
                  </td>
                  <td class="text-center">
                    <span class="badge bg-primary">{{ assignment.problems?.length || 0 }}</span>
                  </td>
                  <td class="text-center">
                    <span class="badge bg-success">{{ assignment.submissions?.length || 0 }}</span>
                  </td>
                  <td class="text-center">
                    <div class="progress-container">
                      <div class="progress" style="height: 20px;">
                        <div 
                          class="progress-bar" 
                          :class="getProgressBarClass(getSubmissionRate(assignment))"
                          :style="{ width: getSubmissionRate(assignment) + '%' }"
                        >
                          {{ getSubmissionRate(assignment) }}%
                        </div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <small class="text-muted">{{ formatDate(assignment.created_at) }}</small>
                  </td>
                  <td>
                    <span v-if="assignment.due_date" 
                          class="badge" 
                          :class="getDueDateBadgeClass(assignment.due_date)">
                      {{ formatDate(assignment.due_date) }}
                    </span>
                    <span v-else class="badge bg-secondary">无截止日期</span>
                  </td>
                  <td>
                    <div class="btn-group btn-group-sm">
                      <button 
                        class="btn btn-outline-primary"
                        @click="editAssignment(assignment.id)"
                        title="编辑作业"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button 
                        class="btn btn-outline-info"
                        @click="viewSubmissions(assignment.id)"
                        title="查看提交"
                      >
                        <i class="bi bi-eye"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="bi bi-inbox display-1 text-muted"></i>
          <h4 class="text-muted mt-3">暂无作业</h4>
          <p class="text-muted">开始创建第一个作业吧！</p>
          <button class="btn btn-primary" @click="createAssignment">
            <i class="bi bi-plus-circle me-1"></i>创建作业
          </button>
        </div>
      </div>

      <!-- 学生列表 -->
      <div v-show="activeTab === 'students'" class="tab-content">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h3>选课学生</h3>
          <button class="btn btn-primary" @click="showEnrollModal = true">
            <i class="bi bi-person-plus me-1"></i>添加学生
          </button>
        </div>

        <div v-if="students.length > 0" class="table-container">
          <div class="table-responsive">
            <table class="table table-hover">
              <thead class="table-light">
                <tr>
                  <th>学生信息</th>
                  <th>邮箱</th>
                  <th>选课时间</th>
                  <th>作业完成情况</th>
                  <th>完成进度</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="student in students" :key="student.id">
                  <td>
                    <div class="d-flex align-items-center">
                      <i class="bi bi-person-circle fs-3 text-primary me-2"></i>
                      <div>
                        <div class="fw-semibold">{{ student.username }}</div>
                        <small class="text-muted">学生ID: {{ student.id }}</small>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="text-muted">{{ student.email }}</span>
                  </td>
                  <td>
                    <small class="text-muted">{{ formatDate(student.enrolled_at) }}</small>
                  </td>
                  <td class="text-center">
                    <div class="d-flex justify-content-center gap-2">
                      <span class="badge bg-success">
                        <i class="bi bi-check-circle me-1"></i>
                        {{ getCompletedAssignments(student.id) }}
                      </span>
                      <span class="badge bg-warning">
                        <i class="bi bi-clock me-1"></i>
                        {{ assignments.length - getCompletedAssignments(student.id) }}
                      </span>
                    </div>
                  </td>
                  <td>
                    <div class="progress-container">
                      <div class="progress" style="height: 20px;">
                        <div 
                          class="progress-bar" 
                          :class="getProgressBarClass(getCompletionRate(student.id))"
                          :style="{ width: getCompletionRate(student.id) + '%' }"
                        >
                          {{ getCompletionRate(student.id) }}%
                        </div>
                      </div>
                      <small class="text-muted">
                        {{ getCompletedAssignments(student.id) }}/{{ assignments.length }} 完成
                      </small>
                    </div>
                  </td>
                  <td>
                    <div class="btn-group btn-group-sm">
                      <button 
                        class="btn btn-outline-info"
                        @click="viewStudentWork(student.id)"
                        title="查看作业"
                      >
                        <i class="bi bi-file-earmark-text"></i>
                      </button>
                      <button 
                        class="btn btn-outline-danger"
                        @click="removeStudent(student.id)"
                        title="移除学生"
                      >
                        <i class="bi bi-person-dash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="bi bi-people display-1 text-muted"></i>
          <h4 class="text-muted mt-3">暂无学生</h4>
          <p class="text-muted">添加学生到这门课程</p>
          <button class="btn btn-primary" @click="showEnrollModal = true">
            <i class="bi bi-person-plus me-1"></i>添加学生
          </button>
        </div>
      </div>
    </div>

    <!-- 添加学生模态框 -->
    <div v-if="showEnrollModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">添加学生</h5>
            <button type="button" class="btn-close" @click="closeEnrollModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">选择学生</label>
              <select class="form-select" v-model="selectedStudentId">
                <option value="">请选择学生</option>
                <option 
                  v-for="student in availableStudents" 
                  :key="student.id" 
                  :value="student.id"
                >
                  {{ student.username }} ({{ student.email }})
                </option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeEnrollModal">取消</button>
            <button 
              type="button" 
              class="btn btn-primary"
              @click="enrollStudent"
              :disabled="!selectedStudentId || isEnrolling"
            >
              {{ isEnrolling ? '添加中...' : '添加学生' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showEnrollModal" class="modal-backdrop fade show"></div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
    </div>

    <!-- 学生作业详情模态框 -->
    <div v-if="showStudentWorkModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-person-circle me-2"></i>
              {{ selectedStudent?.username }} 的作业详情
            </h5>
            <button type="button" class="btn-close" @click="closeStudentWorkModal"></button>
          </div>
          <div class="modal-body">
            <!-- 学生基本信息 -->
            <div class="student-info-card mb-4">
              <div class="row">
                <div class="col-md-6">
                  <div class="info-item">
                    <label class="info-label">学生姓名</label>
                    <div class="info-value">{{ selectedStudent?.username }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-item">
                    <label class="info-label">邮箱地址</label>
                    <div class="info-value">{{ selectedStudent?.email }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-item">
                    <label class="info-label">选课时间</label>
                    <div class="info-value">{{ formatDate(selectedStudent?.enrolled_at) }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-item">
                    <label class="info-label">完成进度</label>
                    <div class="info-value">
                      <div class="progress" style="height: 20px;">
                        <div 
                          class="progress-bar" 
                          :class="getProgressBarClass(getCompletionRate(selectedStudent?.id))"
                          :style="{ width: getCompletionRate(selectedStudent?.id) + '%' }"
                        >
                          {{ getCompletionRate(selectedStudent?.id) }}%
                        </div>
                      </div>
                      <small class="text-muted mt-1 d-block">
                        {{ getCompletedAssignments(selectedStudent?.id) }}/{{ assignments.length }} 作业已完成
                      </small>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 作业列表 -->
            <div class="assignments-section">
              <h6 class="mb-3">
                <i class="bi bi-list-task me-2"></i>
                作业完成情况
              </h6>
              
              <div v-if="isLoadingStudentWork" class="text-center py-3">
                <div class="spinner-border spinner-border-sm text-primary" role="status">
                  <span class="visually-hidden">加载中...</span>
                </div>
                <span class="ms-2">正在加载作业信息...</span>
              </div>
              
              <div v-else-if="studentAssignments.length > 0" class="assignment-list">
                <div 
                  v-for="assignment in studentAssignments" 
                  :key="assignment.id"
                  class="assignment-item"
                >
                  <div class="assignment-header">
                    <div class="assignment-title">
                      <i class="bi bi-file-earmark-text me-2"></i>
                      {{ assignment.title }}
                    </div>
                    <span 
                      class="badge"
                      :class="{
                        'bg-success': assignment.hasSubmitted && assignment.isGraded,
                        'bg-warning': assignment.hasSubmitted && !assignment.isGraded,
                        'bg-secondary': !assignment.hasSubmitted
                      }"
                    >
                      {{ assignment.hasSubmitted ? (assignment.isGraded ? '已评分' : '已提交') : '未提交' }}
                    </span>
                  </div>
                  
                  <div class="assignment-details">
                    <div class="row">
                      <div class="col-md-6">
                        <small class="text-muted">提交时间:</small>
                        <div>{{ assignment.submitTime ? formatDate(assignment.submitTime) : '未提交' }}</div>
                      </div>
                      <div class="col-md-6">
                        <small class="text-muted">得分:</small>
                        <div>
                          <span v-if="assignment.totalScore !== null" class="text-success fw-bold">
                            {{ Math.round(assignment.totalScore * 10) / 10 }}分
                          </span>
                          <span v-else class="text-muted">未评分</span>
                        </div>
                      </div>
                    </div>
                    
                    <div class="mt-2" v-if="assignment.hasSubmitted">
                      <button 
                        class="btn btn-sm btn-outline-primary"
                        @click="viewSpecificAssignmentSubmission(assignment.id)"
                      >
                        <i class="bi bi-eye me-1"></i>查看详情
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-else class="text-center py-3 text-muted">
                <i class="bi bi-inbox"></i>
                暂无作业信息
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeStudentWorkModal">
              关闭
            </button>
            <button 
              type="button" 
              class="btn btn-primary"
              @click="viewAllAssignmentSubmissions"
            >
              <i class="bi bi-list-check me-1"></i>查看所有作业提交
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showStudentWorkModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { teacherAPI } from '../../utils/api'

export default {
  name: 'CourseDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const courseId = route.params.id
    
    // 响应式数据
    const course = ref(null)
    const assignments = ref([])
    const students = ref([])
    const availableStudents = ref([])
    const isLoading = ref(true)
    const activeTab = ref('assignments')
    const showEnrollModal = ref(false)
    const selectedStudentId = ref('')
    const isEnrolling = ref(false)
    const showStudentWorkModal = ref(false)
    const selectedStudent = ref(null)
    const studentAssignments = ref([])
    const isLoadingStudentWork = ref(false)

    // 加载课程详情
    const loadCourseDetail = async () => {
      try {
        isLoading.value = true
        const response = await teacherAPI.getCourse(courseId)
        
        if (response.data.success) {
          const data = response.data.data
          course.value = data.course
          assignments.value = data.assignments || []
          students.value = data.students || []
          availableStudents.value = data.available_students || []
        } else {
          console.error('加载失败:', response.data.message)
          alert('加载课程详情失败')
        }
      } catch (error) {
        console.error('加载课程详情失败:', error)
        alert('加载课程详情失败')
      } finally {
        isLoading.value = false
      }
    }

    // 工具函数
    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    const getSubmissionRate = (assignment) => {
      if (students.value.length === 0) return 0
      const submissionCount = assignment.submissions?.length || 0
      return Math.round((submissionCount / students.value.length) * 100)
    }

    const getCompletedAssignments = (studentId) => {
      return assignments.value.filter(assignment => 
        assignment.submissions?.some(submission => submission.student_id === studentId)
      ).length
    }

    const getCompletionRate = (studentId) => {
      if (assignments.value.length === 0) return 0
      const completed = getCompletedAssignments(studentId)
      return Math.round((completed / assignments.value.length) * 100)
    }

    const getProgressBarClass = (rate) => {
      if (rate >= 80) return 'bg-success'
      if (rate >= 60) return 'bg-warning'
      if (rate >= 40) return 'bg-danger'
      return 'bg-secondary'
    }

    const getDueDateBadgeClass = (dueDate) => {
      if (!dueDate) return 'bg-secondary'
      const now = new Date()
      const due = new Date(dueDate)
      const diffDays = Math.ceil((due - now) / (1000 * 60 * 60 * 24))
      
      if (diffDays < 0) return 'bg-danger'
      if (diffDays <= 3) return 'bg-warning'
      return 'bg-success'
    }

    // 操作函数
    const createAssignment = () => {
      router.push(`/teacher/create-assignment?course=${courseId}`)
    }

    const editAssignment = (assignmentId) => {
      router.push(`/teacher/assignments/${assignmentId}/edit`)
    }

    const viewSubmissions = (assignmentId) => {
      router.push(`/teacher/assignments/${assignmentId}/submissions`)
    }

    const viewStudentWork = (studentId) => {
      // 获取学生信息
      const student = students.value.find(s => s.id === studentId)
      if (!student) {
        alert('找不到学生信息')
        return
      }
      
      // 设置选中的学生并显示作业详情模态框
      selectedStudent.value = student
      loadStudentAssignments(studentId)
      showStudentWorkModal.value = true
    }

    const loadStudentAssignments = async (studentId) => {
      try {
        isLoadingStudentWork.value = true
        studentAssignments.value = []
        
        // 获取该学生在当前课程中的作业完成情况
        const assignmentPromises = assignments.value.map(async (assignment) => {
          try {
            // 检查学生是否有提交这个作业
            const submissionResponse = await teacherAPI.getSubmissions(assignment.id)
            if (submissionResponse.data.success) {
              const submissions = submissionResponse.data.data.submissions
              const studentSubmission = submissions.find(sub => sub.student_id === studentId)
              
              return {
                ...assignment,
                submission: studentSubmission || null,
                hasSubmitted: !!studentSubmission,
                submitTime: studentSubmission?.submitted_at || null,
                totalScore: studentSubmission?.total_score || null,
                isGraded: studentSubmission?.is_graded || false
              }
            }
          } catch (error) {
            console.error(`获取作业 ${assignment.id} 提交情况失败:`, error)
            return {
              ...assignment,
              submission: null,
              hasSubmitted: false,
              submitTime: null,
              totalScore: null,
              isGraded: false
            }
          }
        })
        
        const results = await Promise.all(assignmentPromises)
        studentAssignments.value = results
        
      } catch (error) {
        console.error('加载学生作业失败:', error)
        alert('加载学生作业失败')
      } finally {
        isLoadingStudentWork.value = false
      }
    }

    const closeStudentWorkModal = () => {
      showStudentWorkModal.value = false
      selectedStudent.value = null
      studentAssignments.value = []
    }

    const viewAssignmentDetail = (assignmentId) => {
      router.push(`/teacher/assignments/${assignmentId}/submissions`)
    }

    const viewSpecificAssignmentSubmission = (assignmentId) => {
      router.push(`/teacher/assignments/${assignmentId}/submissions`)
    }

    const viewAllAssignmentSubmissions = () => {
      // 跳转到作业管理页面，显示该课程的所有作业
      router.push(`/teacher/assignments?course=${courseId}`)
    }

    const removeStudent = async (studentId) => {
      if (!confirm('确定要移除这个学生吗？')) return
      
      try {
        const response = await teacherAPI.unenrollStudent(courseId, studentId)
        if (response.data.success) {
          await loadCourseDetail()
          alert('学生移除成功')
        } else {
          alert(response.data.message || '移除失败')
        }
      } catch (error) {
        console.error('移除学生失败:', error)
        alert('移除学生失败')
      }
    }

    const enrollStudent = async () => {
      if (!selectedStudentId.value) return
      
      try {
        isEnrolling.value = true
        const response = await teacherAPI.enrollStudent(courseId, {
          student_id: selectedStudentId.value
        })
        
        if (response.data.success) {
          await loadCourseDetail()
          closeEnrollModal()
          alert('学生添加成功')
        } else {
          alert(response.data.message || '添加失败')
        }
      } catch (error) {
        console.error('添加学生失败:', error)
        alert('添加学生失败')
      } finally {
        isEnrolling.value = false
      }
    }

    const closeEnrollModal = () => {
      showEnrollModal.value = false
      selectedStudentId.value = ''
    }

    // 页面加载
    onMounted(() => {
      loadCourseDetail()
    })

    return {
      course,
      assignments,
      students,
      availableStudents,
      isLoading,
      activeTab,
      showEnrollModal,
      selectedStudentId,
      isEnrolling,
      showStudentWorkModal,
      selectedStudent,
      studentAssignments,
      isLoadingStudentWork,
      formatDate,
      getSubmissionRate,
      getCompletedAssignments,
      getCompletionRate,
      getProgressBarClass,
      getDueDateBadgeClass,
      createAssignment,
      editAssignment,
      viewSubmissions,
      viewStudentWork,
      removeStudent,
      enrollStudent,
      closeEnrollModal,
      closeStudentWorkModal,
      viewAssignmentDetail,
      viewSpecificAssignmentSubmission,
      viewAllAssignmentSubmissions
    }
  }
}
</script>

<style scoped>
/* 页面布局 */
.course-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  margin-bottom: 2rem;
}

/* 统计卡片 */
.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
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

.stat-content h3 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
}

.stat-content p {
  margin: 0;
  color: #6c757d;
}

/* 选项卡 */
.nav-pills .nav-link {
  background: none;
  border: 2px solid #e9ecef;
  color: #6c757d;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  margin-right: 0.5rem;
  transition: all 0.2s ease;
}

.nav-pills .nav-link.active {
  background: #007bff;
  border-color: #007bff;
  color: white;
}

.nav-pills .nav-link:hover {
  border-color: #007bff;
  color: #007bff;
}

/* 表格样式 */
.table-container {
  margin-bottom: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  overflow: hidden;
}

.table-responsive {
  border-radius: 12px;
}

.table {
  margin-bottom: 0;
  border-collapse: separate;
  border-spacing: 0;
}

.table th {
  background-color: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
  font-weight: 600;
  color: #495057;
  padding: 1rem 0.75rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.table td {
  padding: 0.75rem;
  border-bottom: 1px solid #dee2e6;
  vertical-align: middle;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
  transition: background-color 0.2s ease;
}

.table tbody tr:last-child td {
  border-bottom: none;
}

/* 进度条样式 */
.progress-container {
  min-width: 120px;
}

.progress {
  height: 20px;
  background-color: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 10px;
  transition: width 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

.progress-bar.bg-success {
  background: linear-gradient(45deg, #28a745, #20c997);
}

.progress-bar.bg-warning {
  background: linear-gradient(45deg, #ffc107, #fd7e14);
}

.progress-bar.bg-danger {
  background: linear-gradient(45deg, #dc3545, #e74c3c);
}

.progress-bar.bg-secondary {
  background: linear-gradient(45deg, #6c757d, #adb5bd);
}

/* 徽章样式 */
.badge {
  font-size: 0.75rem;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
}

/* 按钮组样式 */
.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  border-radius: 4px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

/* 模态框 */
.modal {
  background: rgba(0,0,0,0.5);
}

/* 加载状态 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255,255,255,0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .course-detail {
    padding: 1rem;
  }
  
  .stat-card {
    padding: 1rem;
  }
  
  .table th,
  .table td {
    padding: 0.5rem;
    font-size: 0.875rem;
  }
  
  .progress-container {
    min-width: 80px;
  }
  
  .btn-group-sm .btn {
    padding: 0.2rem 0.4rem;
    font-size: 0.75rem;
  }
}

@media (max-width: 576px) {
  .table-responsive {
    font-size: 0.8rem;
  }
  
  .badge {
    font-size: 0.65rem;
    padding: 0.25rem 0.4rem;
  }
  
  .progress {
    height: 16px;
  }
  
  .progress-bar {
    font-size: 0.65rem;
  }
}

/* 学生作业详情模态框样式 */
.student-info-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #e9ecef;
}

.info-item {
  margin-bottom: 1rem;
}

.info-label {
  font-weight: 600;
  color: #495057;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  display: block;
}

.info-value {
  color: #212529;
  font-size: 1rem;
}

.assignments-section {
  border-top: 1px solid #dee2e6;
  padding-top: 1rem;
}

.assignment-list {
  max-height: 400px;
  overflow-y: auto;
}

.assignment-item {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  transition: box-shadow 0.2s ease;
}

.assignment-item:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.assignment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.assignment-title {
  font-weight: 600;
  color: #495057;
  font-size: 1rem;
  display: flex;
  align-items: center;
}

.assignment-details {
  color: #6c757d;
  font-size: 0.875rem;
}
</style>


