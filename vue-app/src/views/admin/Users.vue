<template>
  <div class="admin-users">
    <div class="page-header">
      <h1><i class="bi bi-people me-2"></i>用户管理</h1>
      <p>添加和管理教师与学生账户</p>
    </div>

    <div class="row">
      <!-- 添加用户表单 -->
      <div class="col-md-4">
        <div class="card mb-4">
          <div class="card-header"><h5 class="mb-0">添加新用户</h5></div>
          <div class="card-body">
            <form @submit.prevent="addUser">
              <div class="mb-3">
                <label class="form-label">用户名</label>
                <input v-model="newUser.username" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">邮箱</label>
                <input v-model="newUser.email" type="email" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">密码</label>
                <input v-model="newUser.password" type="password" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">角色</label>
                <select v-model="newUser.role" class="form-select" required>
                  <option value="" disabled>选择角色</option>
                  <option value="teacher">教师</option>
                  <option value="student">学生</option>
                </select>
              </div>
              <button class="btn btn-primary w-100" type="submit" :disabled="isSubmitting">
                <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>添加用户
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- 用户列表 -->
      <div class="col-md-8">
        <div class="alert alert-info mb-3">
          <strong>数据状态:</strong>
          总用户: {{ allUsers.length }} |
          教师: {{ teacherCount }} |
          学生: {{ studentCount }} |
          当前视图: {{ currentView }}
          <br><small>最后更新: {{ lastUpdateTime }}</small>
        </div>

        <div class="btn-group mb-3">
          <button
            class="btn"
            :class="currentView==='teacher'? 'btn-primary':'btn-outline-primary'"
            @click="setCurrentView('teacher')"
          >教师列表 ({{ teacherCount }})</button>
          <button
            class="btn"
            :class="currentView==='student'? 'btn-primary':'btn-outline-primary'"
            @click="setCurrentView('student')"
          >学生列表 ({{ studentCount }})</button>
          <button class="btn btn-outline-secondary" @click="refreshData">
            <i class="bi bi-arrow-clockwise me-1"></i>刷新数据
          </button>
        </div>

        <div class="card">
          <div class="card-header bg-light">
            <h5 class="mb-0">{{ currentView==='teacher'? '教师':'学生' }}列表 ({{ currentUsers.length }})</h5>
          </div>
          <div class="card-body">
            <div v-if="isLoading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status"></div>
              <p class="mt-2">正在加载用户数据...</p>
            </div>
            <div v-else-if="currentUsers.length" class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>ID</th><th>用户名</th><th>邮箱</th><th>角色</th><th>创建时间</th><th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="u in currentUsers" :key="u.id">
                    <td>{{ u.id }}</td>
                    <td>{{ u.username }}</td>
                    <td>{{ u.email }}</td>
                    <td>
                      <span class="badge" :class="u.role==='teacher'? 'bg-primary':'bg-success'">
                        {{ u.role==='teacher'? '教师':'学生' }}
                      </span>
                    </td>
                    <td>{{ formatDate(u.created_at) }}</td>
                    <td>
                      <button class="btn btn-sm btn-outline-primary me-1" @click="openEditModal(u)">
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button class="btn btn-sm btn-outline-danger" @click="handleDelete(u)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="text-center py-4 text-muted">
              暂无{{ currentView==='teacher'? '教师':'学生' }}数据
            </div>
          </div>
        </div>

        <!-- 编辑用户模态框 -->
        <div v-if="showEditModal" class="custom-modal-backdrop" @click="closeEditModal">
          <div class="custom-modal" @click.stop>
            <div class="custom-modal-content">
              <div class="custom-modal-header">
                <h5 class="modal-title">编辑用户</h5>
                <button type="button" class="btn-close" @click="closeEditModal"></button>
              </div>
              <div class="custom-modal-body">
                <form @submit.prevent="updateUser">
                  <div class="mb-3">
                    <label class="form-label">用户名</label>
                    <input v-model="editing.username" class="form-control" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label">邮箱</label>
                    <input v-model="editing.email" class="form-control" required />
                  </div>
                </form>
              </div>
              <div class="custom-modal-footer">
                <button class="btn btn-secondary" @click="closeEditModal">取消</button>
                <button class="btn btn-primary" @click="updateUser" :disabled="isUpdating">
                  <span v-if="isUpdating" class="spinner-border spinner-border-sm me-2"></span>保存修改
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import api from '../../utils/api'

export default {
  name: 'AdminUsers',
  setup() {
    const isLoading = ref(false)
    const isSubmitting = ref(false)
    const isUpdating = ref(false)
    const currentView = ref('teacher')
    const allUsers = ref([])
    const lastUpdateTime = ref('')

    const showEditModal = ref(false)
    const editing = reactive({ id:null, username:'', email:'', role:'' })

    const newUser = reactive({ username:'', email:'', password:'', role:'' })

    const teacherCount = computed(()=> allUsers.value.filter(u=>u.role==='teacher').length)
    const studentCount = computed(()=> allUsers.value.filter(u=>u.role==='student').length)
    const currentUsers = computed(()=>
      allUsers.value.filter(u=> u.role===currentView.value)
    )

    const loadUsers = async()=>{
      isLoading.value = true
      try{
        const res = await api.get('/admin/users')
        const { teachers, students } = res.data.data
        allUsers.value = [
          ...teachers.map(t => ({...t, role: 'teacher'})),
          ...students.map(s => ({...s, role: 'student'}))
        ]
        lastUpdateTime.value = new Date().toLocaleTimeString()
      }catch(e){
        alert('加载失败:'+e.message)
      }finally{ isLoading.value=false }
    }

    const addUser = async()=>{
      if(!newUser.username||!newUser.email||!newUser.password||!newUser.role) return alert('请填写完整')
      isSubmitting.value=true
      try {
        await api.post('/admin/users', newUser)
        await loadUsers()
        Object.assign(newUser,{username:'',email:'',password:'',role:''})
        alert('用户创建成功')
      } catch(e) {
        alert('创建失败:'+e.message)
      } finally {
        isSubmitting.value=false
      }
    }

    const openEditModal = (u)=>{
      Object.assign(editing,u)
      showEditModal.value = true
    }
    
    const updateUser = async()=>{
      if(!editing.username||!editing.email) return alert('请填写完整')
      isUpdating.value=true
      try {
        await api.put(`/admin/users/${editing.id}`,{
          username:editing.username,
          email:editing.email,
          role:editing.role
        })
        await loadUsers()
        showEditModal.value=false
        alert('用户更新成功')
      } catch(e) {
        alert('更新失败:'+e.message)
      } finally {
        isUpdating.value=false
      }
    }
    
    const closeEditModal = ()=> showEditModal.value=false

    const handleDelete = async(u)=>{
      if(!confirm(`确定要删除用户 ${u.username}?`)) return
      try {
        await api.delete(`/admin/users/${u.id}`)
        await loadUsers()
        alert('用户删除成功')
      } catch(e) {
        alert('删除失败:'+e.message)
      }
    }
    
    const setCurrentView = v=> currentView.value=v
    const refreshData = ()=> loadUsers()
    const formatDate = s=> new Date(s).toLocaleDateString('zh-CN')

    onMounted(loadUsers)
    return{
      isLoading,isSubmitting,isUpdating,currentView,allUsers,lastUpdateTime,
      newUser,teacherCount,studentCount,currentUsers,
      addUser,handleDelete,setCurrentView,refreshData,
      showEditModal,editing,openEditModal,updateUser,closeEditModal,formatDate
    }
  }
}
</script>

<style scoped>
.page-header { margin-bottom:2rem; padding-bottom:1rem; border-bottom:1px solid #dee2e6; }

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