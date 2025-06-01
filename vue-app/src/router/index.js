import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated, isAdmin, isTeacher, isStudent, initializeAuth } from '../stores/auth'

// 首页组件
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import ApiTest from '../views/ApiTest.vue'

// 功能页面组件
import ProblemGeneration from '../views/ProblemGeneration.vue'
import MultiUpload from '../views/MultiUpload.vue'

// 通用组件
import UserProfile from '../components/UserProfile.vue'

// Admin views
import AdminDashboard from '../views/admin/Dashboard.vue'
import AdminUsers from '../views/admin/Users.vue'
import AdminCourses from '../views/admin/Courses.vue'

// Teacher views
import TeacherDashboard from '../views/teacher/Dashboard.vue'
import TeacherCourses from '../views/teacher/Courses.vue'
import TeacherCourseDetail from '../views/teacher/CourseDetail.vue'
import TeacherAssignments from '../views/teacher/Assignments.vue'
import CreateAssignment from '../views/teacher/CreateAssignment.vue'
import EditAssignment from '../views/teacher/EditAssignment.vue'
import EditProblem from '../views/teacher/EditProblem.vue'
import ViewSubmissions from '../views/teacher/ViewSubmissions.vue'

// Student views
import StudentDashboard from '../views/student/Dashboard.vue'
import ViewAssignment from '../views/student/ViewAssignment.vue'
import StudentCourseDetail from '../views/student/CourseDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: '智能教学系统' }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { 
      title: '用户登录',
      requiresGuest: true // 只有未登录用户可以访问
    }
  },
  {
    path: '/api-test',
    name: 'ApiTest',
    component: ApiTest,
    meta: { title: 'API测试' }
  },
  {
    path: '/problem-generation',
    name: 'ProblemGeneration',
    component: ProblemGeneration,
    meta: { 
      title: '智能出题',
      requiresAuth: true
    }
  },
  {
    path: '/multi-upload',
    name: 'MultiUpload',
    component: MultiUpload,
    meta: { 
      title: '智能批改',
      requiresAuth: true
    }
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { 
      title: '个人信息',
      requiresAuth: true
    }
  },
  // 管理员路由
  {
    path: '/admin',
    redirect: '/admin/dashboard',
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { 
      title: '管理员面板',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: AdminUsers,
    meta: { 
      title: '用户管理',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/courses',
    name: 'AdminCourses',
    component: AdminCourses,
    meta: { 
      title: '课程管理',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  // 教师路由
  {
    path: '/teacher',
    redirect: '/teacher/dashboard',
    meta: { requiresAuth: true, requiresTeacher: true }
  },
  {
    path: '/teacher/dashboard',
    name: 'TeacherDashboard',
    component: TeacherDashboard,
    meta: { 
      title: '教师面板',
      requiresAuth: true,
      requiresTeacher: true
    }
  },
  {
    path: '/teacher/courses',
    name: 'TeacherCourses',
    component: TeacherCourses,
    meta: { 
      title: '我的课程',
      requiresAuth: true,
      requiresTeacher: true
    }
  },
  {
    path: '/teacher/courses/:id',
    name: 'TeacherCourseDetail',
    component: TeacherCourseDetail,
    meta: { 
      title: '课程详情',
      requiresAuth: true,
      requiresTeacher: true
    }
  },
  {
    path: '/teacher/assignments',
    name: 'TeacherAssignments',
    component: TeacherAssignments,
    meta: { 
      title: '作业管理',
      requiresAuth: true,
      requiresTeacher: true
    }
  },
  {
    path: '/teacher/create-assignment',
    name: 'CreateAssignment',
    component: CreateAssignment,
    meta: { 
      title: '创建作业',
      requiresAuth: true,
      requiresTeacher: true
    }
  },
  {
    path: '/teacher/assignments/:id/edit',
    name: 'EditAssignment',
    component: EditAssignment,
    meta: { 
      title: '编辑作业',
      requiresAuth: true,
      requiresTeacher: true
    }
  },
  {
    path: '/teacher/problems/:id/edit',
    name: 'EditProblem',
    component: EditProblem,
    meta: { 
      title: '编辑题目',
      requiresAuth: true,
      requiresTeacher: true
    }
  },
  {
    path: '/teacher/assignments/:id/submissions',
    name: 'ViewSubmissions',
    component: ViewSubmissions,
    meta: { 
      title: '查看提交',
      requiresAuth: true,
      requiresTeacher: true
    }
  },
  // 学生路由
  {
    path: '/student/dashboard',
    name: 'StudentDashboard',
    component: StudentDashboard,
    meta: { 
      title: '学生面板',
      requiresAuth: true,
      requiresStudent: true
    }
  },
  {
    path: '/student/assignment/:id',
    name: 'ViewAssignment',
    component: ViewAssignment,
    meta: { 
      title: '查看作业',
      requiresAuth: true,
      requiresStudent: true
    }
  },
  {
    path: '/student/course/:id',
    name: 'StudentCourseDetail',
    component: StudentCourseDetail,
    meta: { 
      title: '课程详情',
      requiresAuth: true,
      requiresStudent: true
    }
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: {
      template: `
        <div class="container mt-5">
          <div class="row justify-content-center">
            <div class="col-md-6 text-center">
              <i class="bi bi-exclamation-triangle display-1 text-warning"></i>
              <h1 class="mt-3">404 - 页面未找到</h1>
              <p class="text-muted">抱歉，您访问的页面不存在。</p>
              <router-link to="/" class="btn btn-primary">
                <i class="bi bi-house me-2"></i>返回首页
              </router-link>
            </div>
          </div>
        </div>
      `
    },
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 初始化认证状态（仅在首次访问时）
  if (!isAuthenticated.value && localStorage.getItem('user')) {
    await initializeAuth()
  }

  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 智能教学系统`
  }

  // 检查是否需要登录
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
    return
  }

  // 检查是否只允许未登录用户访问（如登录页）
  if (to.meta.requiresGuest && isAuthenticated.value) {
    next('/')
    return
  }

  // 检查管理员权限
  if (to.meta.requiresAdmin && !isAdmin.value) {
    next('/')
    return
  }

  // 检查教师权限
  if (to.meta.requiresTeacher && !isTeacher.value) {
    next('/')
    return
  }

  // 检查学生权限
  if (to.meta.requiresStudent && !isStudent.value) {
    next('/')
    return
  }

  next()
})

export default router 