<template>
  <div class="admin-courses">
    <div class="page-header">
      <h1><i class="bi bi-journal-album me-2"></i>课程管理</h1>
      <p>创建和管理系统课程</p>
    </div>

    <div class="row">
      <!-- 添加课程表单 -->
      <div class="col-md-4">
        <div class="card mb-4">
          <div class="card-header">
            <h5 class="mb-0">创建新课程</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="addCourse">
              <div class="mb-3">
                <label for="courseName" class="form-label">课程名称</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="courseName" 
                  v-model="newCourse.name" 
                  required
                >
              </div>
              <div class="mb-3">
                <label for="courseDescription" class="form-label">课程描述</label>
                <textarea 
                  class="form-control" 
                  id="courseDescription" 
                  v-model="newCourse.description" 
                  rows="3"
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="teacherId" class="form-label">授课教师</label>
                <select 
                  class="form-select" 
                  id="teacherId" 
                  v-model="newCourse.teacher_id" 
                  required
                >
                  <option value="" disabled>选择教师</option>
                  <option 
                    v-for="teacher in teachers" 
                    :key="teacher.id" 
                    :value="teacher.id"
                  >
                    {{ teacher.username }}
                  </option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary w-100" :disabled="isSubmitting">
                <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                创建课程
              </button>
            </form>
          </div>
        </div>
      </div>
      
      <!-- 课程列表 -->
      <div class="col-md-8">
        <div class="card">
          <div class="card-header bg-light">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="mb-0">课程列表</h5>
              <div class="input-group" style="width: 250px;">
                <input 
                  type="text" 
                  class="form-control" 
                  placeholder="搜索课程..." 
                  v-model="searchQuery"
                >
                <button class="btn btn-outline-secondary" type="button">
                  <i class="bi bi-search"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div v-if="filteredCourses.length > 0" class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>课程名称</th>
                    <th>授课教师</th>
                    <th>创建时间</th>
                    <th>学生数量</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="course in filteredCourses" :key="course.id">
                    <td>{{ course.name }}</td>
                    <td>{{ course.teacher_name }}</td>
                    <td>{{ formatDate(course.created_at) }}</td>
                    <td>{{ course.students_count || 0 }}</td>
                    <td>
                      <div class="btn-group btn-group-sm" role="group">
                        <button 
                          class="btn btn-outline-info" 
                          @click="viewCourse(course)"
                          title="查看详情"
                        >
                          <i class="bi bi-eye"></i>
                        </button>
                        <button 
                          class="btn btn-outline-primary" 
                          @click="editCourse(course)"
                          title="编辑"
                        >
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button 
                          class="btn btn-outline-danger" 
                          @click="deleteCourse(course)"
                          title="删除"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="text-center py-4">
              <p class="text-muted">暂无课程数据</p>
              <button class="btn btn-outline-primary mt-2" @click="scrollToForm">
                <i class="bi bi-plus-circle me-1"></i>创建第一个课程
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑课程模态框 -->
    <div v-if="showEditModal" class="custom-modal-backdrop" @click="closeEditModal">
      <div class="custom-modal" @click.stop>
        <div class="custom-modal-content">
          <div class="custom-modal-header">
            <h5 class="modal-title">编辑课程</h5>
            <button type="button" class="btn-close" @click="closeEditModal"></button>
          </div>
          <div class="custom-modal-body">
            <form @submit.prevent="updateCourse">
              <div class="mb-3">
                <label for="editCourseName" class="form-label">课程名称</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="editCourseName" 
                  v-model="editingCourse.name" 
                  required
                >
              </div>
              <div class="mb-3">
                <label for="editCourseDescription" class="form-label">课程描述</label>
                <textarea 
                  class="form-control" 
                  id="editCourseDescription" 
                  v-model="editingCourse.description" 
                  rows="3"
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="editTeacherId" class="form-label">授课教师</label>
                <select 
                  class="form-select" 
                  id="editTeacherId" 
                  v-model="editingCourse.teacher_id"
                >
                  <option value="" disabled>选择教师</option>
                  <option 
                    v-for="teacher in teachers" 
                    :key="teacher.id" 
                    :value="teacher.id"
                  >
                    {{ teacher.username }}
                  </option>
                </select>
              </div>
            </form>
          </div>
          <div class="custom-modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeEditModal">取消</button>
            <button type="button" class="btn btn-primary" @click="updateCourse" :disabled="isUpdating">
              <span v-if="isUpdating" class="spinner-border spinner-border-sm me-2"></span>
              保存修改
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 课程详情模态框 -->
    <div v-if="showDetailModal" class="custom-modal-backdrop" @click="closeDetailModal">
      <div class="custom-modal custom-modal-lg" @click.stop>
        <div class="custom-modal-content">
          <div class="custom-modal-header">
            <h5 class="modal-title">课程详情</h5>
            <button type="button" class="btn-close" @click="closeDetailModal"></button>
          </div>
          <div class="custom-modal-body">
            <div class="row">
              <div class="col-md-6">
                <h6>基本信息</h6>
                <dl class="row">
                  <dt class="col-sm-4">课程名称:</dt>
                  <dd class="col-sm-8">{{ viewingCourse.name }}</dd>
                  
                  <dt class="col-sm-4">授课教师:</dt>
                  <dd class="col-sm-8">{{ viewingCourse.teacher_name }}</dd>
                  
                  <dt class="col-sm-4">创建时间:</dt>
                  <dd class="col-sm-8">{{ formatDate(viewingCourse.created_at) }}</dd>
                  
                  <dt class="col-sm-4">学生数量:</dt>
                  <dd class="col-sm-8">{{ viewingCourse.students_count || 0 }}</dd>
                </dl>
              </div>
              <div class="col-md-6">
                <h6>课程描述</h6>
                <p>{{ viewingCourse.description || '暂无描述' }}</p>
              </div>
            </div>
          </div>
          <div class="custom-modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDetailModal">关闭</button>
            <button type="button" class="btn btn-primary" @click="editCourse(viewingCourse)">编辑课程</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, reactive, computed } from 'vue'
import api from '../../utils/api'

export default {
  name: 'AdminCourses',
  setup() {
    const courses = ref([])
    const teachers = ref([])
    const searchQuery = ref('')
    const isSubmitting = ref(false)
    const isUpdating = ref(false)
    const showEditModal = ref(false)
    const showDetailModal = ref(false)

    const newCourse = reactive({
      name: '',
      description: '',
      teacher_id: ''
    })

    const editingCourse = reactive({
      id: null,
      name: '',
      description: '',
      teacher_id: ''
    })

    const viewingCourse = reactive({
      id: null,
      name: '',
      description: '',
      teacher_name: '',
      created_at: '',
      students_count: 0
    })

    const filteredCourses = computed(() => {
      if (!searchQuery.value) return courses.value
      
      const query = searchQuery.value.toLowerCase()
      return courses.value.filter(course => 
        course.name.toLowerCase().includes(query) ||
        course.teacher_name.toLowerCase().includes(query)
      )
    })

    const loadCoursesAndTeachers = async () => {
      try {
        const response = await api.get('/admin/courses')
        if (response.data.success) {
          courses.value = response.data.data.courses
          teachers.value = response.data.data.teachers
        }
      } catch (error) {
        console.error('加载课程数据失败:', error)
        // 使用模拟数据
        courses.value = [
          {
            id: 1,
            name: '高等数学',
            description: '高等数学基础课程',
            teacher_name: '张老师',
            teacher_id: 1,
            students_count: 25,
            created_at: '2024-01-15'
          },
          {
            id: 2,
            name: '线性代数',
            description: '线性代数与矩阵论',
            teacher_name: '李老师',
            teacher_id: 2,
            students_count: 18,
            created_at: '2024-01-14'
          }
        ]
        teachers.value = [
          { id: 1, username: '张老师' },
          { id: 2, username: '李老师' }
        ]
      }
    }

    const addCourse = async () => {
      if (!newCourse.name || !newCourse.teacher_id) {
        alert('请填写所有必填字段')
        return
      }

      isSubmitting.value = true
      try {
        await api.post('/admin/courses', newCourse)
        
        // 重新加载课程列表
        await loadCoursesAndTeachers()
        
        // 清空表单
        Object.assign(newCourse, {
          name: '',
          description: '',
          teacher_id: ''
        })
        
        alert('课程创建成功')
      } catch (error) {
        console.error('创建课程失败:', error)
        alert('创建课程失败: ' + (error.response?.data?.message || error.message))
      } finally {
        isSubmitting.value = false
      }
    }

    const editCourse = (course) => {
      Object.assign(editingCourse, {
        id: course.id,
        name: course.name,
        description: course.description,
        teacher_id: course.teacher_id
      })
      
      // 关闭详情模态框（如果打开）
      closeDetailModal()
      
      // 显示编辑模态框
      showEditModal.value = true
    }

    const updateCourse = async () => {
      if (!editingCourse.name || !editingCourse.teacher_id) {
        alert('请填写所有必填字段')
        return
      }

      isUpdating.value = true
      try {
        await api.put(`/admin/courses/${editingCourse.id}`, {
          name: editingCourse.name,
          description: editingCourse.description,
          teacher_id: editingCourse.teacher_id
        })
        
        // 重新加载课程列表
        await loadCoursesAndTeachers()
        
        closeEditModal()
        alert('课程更新成功')
      } catch (error) {
        console.error('更新课程失败:', error)
        alert('更新课程失败: ' + (error.response?.data?.message || error.message))
      } finally {
        isUpdating.value = false
      }
    }

    const deleteCourse = async (course) => {
      if (!confirm(`确定要删除课程 "${course.name}" 吗？`)) {
        return
      }

      try {
        await api.delete(`/admin/courses/${course.id}`)
        
        // 重新加载课程列表
        await loadCoursesAndTeachers()
        
        alert('课程删除成功')
      } catch (error) {
        console.error('删除课程失败:', error)
        alert('删除课程失败: ' + (error.response?.data?.message || error.message))
      }
    }

    const viewCourse = (course) => {
      Object.assign(viewingCourse, course)
      
      // 显示详情模态框
      showDetailModal.value = true
    }

    const closeEditModal = () => {
      showEditModal.value = false
    }

    const closeDetailModal = () => {
      showDetailModal.value = false
    }

    const scrollToForm = () => {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    onMounted(() => {
      loadCoursesAndTeachers()
    })

    return {
      courses,
      teachers,
      filteredCourses,
      searchQuery,
      newCourse,
      editingCourse,
      viewingCourse,
      isSubmitting,
      isUpdating,
      showEditModal,
      showDetailModal,
      addCourse,
      editCourse,
      updateCourse,
      deleteCourse,
      viewCourse,
      closeEditModal,
      closeDetailModal,
      scrollToForm,
      formatDate
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

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.card-header {
  background-color: #f8f9fa !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
}

.btn-group-sm > .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

/* 自定义模态框样式 */
.custom-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.custom-modal {
  background-color: white;
  border-radius: 0.3rem;
  width: 500px;
  max-width: 95%;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.custom-modal-lg {
  width: 800px;
}

.custom-modal-content {
  display: flex;
  flex-direction: column;
}

.custom-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.custom-modal-body {
  padding: 1rem;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

.custom-modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 1rem;
  border-top: 1px solid #dee2e6;
  gap: 0.5rem;
}
</style>
