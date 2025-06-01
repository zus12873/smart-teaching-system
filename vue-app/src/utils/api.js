import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api', // 使用相对路径，通过Vite代理
  timeout: 300000, // 300秒超时
  withCredentials: true, // 支持跨域cookie
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    console.log('发送请求:', config.method?.toUpperCase(), config.url)
    
    // 如果是文件上传，修改Content-Type
    if (config.data instanceof FormData) {
      config.headers['Content-Type'] = 'multipart/form-data'
    }
    
    return config
  },
  error => {
    // 对请求错误做些什么
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    console.log('收到响应:', response.status, response.config.url)
    return response
  },
  error => {
    // 对响应错误做点什么
    console.error('响应错误:', error.response?.status, error.response?.data || error.message)
    
    if (error.code === 'ERR_NETWORK') {
      console.error('网络错误：可能是CORS问题或服务器未启动')
    } else if (error.response?.status === 401) {
      // 未授权，清除本地状态并重定向到登录页面
      console.warn('用户未授权，可能需要重新登录')
      
      // 清除本地存储的用户信息
      localStorage.removeItem('user')
      
      // 如果当前不在登录页面，则重定向到登录页面
      if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
        window.location.href = `/login?redirect=${encodeURIComponent(window.location.pathname)}`
      }
    } else if (error.response?.status === 403) {
      // 禁止访问
      console.warn('用户无权访问此资源')
    } else if (error.response?.status >= 500) {
      // 服务器错误
      console.error('服务器内部错误')
    }
    
    return Promise.reject(error)
  }
)

// 导出API实例
export default api

// 导出一些常用的API方法
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  logout: () => api.post('/auth/logout'),
  getCurrentUser: () => api.get('/auth/current')
}

export const adminAPI = {
  getDashboard: () => api.get('/admin/dashboard'),
  getUsers: () => api.get('/admin/users'),
  createUser: (userData) => api.post('/admin/users', userData),
  getUser: (userId) => api.get(`/admin/users/${userId}`),
  updateUser: (userId, userData) => api.put(`/admin/users/${userId}`, userData),
  deleteUser: (userId) => api.delete(`/admin/users/${userId}`),
  getCourses: () => api.get('/admin/courses'),
  createCourse: (courseData) => api.post('/admin/courses', courseData),
  getCourse: (courseId) => api.get(`/admin/courses/${courseId}`),
  updateCourse: (courseId, courseData) => api.put(`/admin/courses/${courseId}`, courseData),
  deleteCourse: (courseId) => api.delete(`/admin/courses/${courseId}`)
}

export const workflowAPI = {
  runWorkflow: (formData) => api.post('/run_workflow', formData),
  runMultiWorkflow: (formData) => api.post('/run_multi_workflow', formData),
  getTeacherCourses: () => api.get('/teacher/courses'),
  saveGeneratedAssignment: (assignmentData) => api.post('/save_generated_assignment', assignmentData)
}

export const teacherAPI = {
  // 获取教师仪表板数据
  getDashboard: () => api.get('/teacher/dashboard'),
  
  // 获取教师课程列表
  getCourses: () => api.get('/teacher/courses'),
  
  // 作业管理
  getAssignments: () => api.get('/teacher/assignments'),
  createAssignment: (assignmentData) => api.post('/teacher/assignments', assignmentData),
  getAssignment: (assignmentId) => api.get(`/teacher/assignments/${assignmentId}`),
  updateAssignment: (assignmentId, assignmentData) => api.put(`/teacher/assignments/${assignmentId}`, assignmentData),
  deleteAssignment: (assignmentId) => api.delete(`/teacher/assignments/${assignmentId}`),
  
  // 题目管理
  addProblem: (assignmentId, problemData) => api.post(`/teacher/assignments/${assignmentId}/problems`, problemData),
  getProblem: (problemId) => api.get(`/teacher/problems/${problemId}`),
  updateProblem: (problemId, problemData) => api.put(`/teacher/problems/${problemId}`, problemData),
  deleteProblem: (problemId) => api.delete(`/teacher/problems/${problemId}`),
  
  // 智能生成题目
  generateProblem: (assignmentId, generateData) => api.post('/teacher/generate_problem', {
    assignment_id: assignmentId,
    ...generateData
  }),
  
  // 智能生成题目（支持文件上传）
  generateProblemWithFile: (formData) => api.post('/teacher/generate_problem', formData),
  
  // 保存生成的题目
  saveGeneratedProblem: (assignmentId, problemText) => api.post(`/teacher/assignments/${assignmentId}/problems`, {
    problem_text: problemText,
    reference_answer: '',
    grading_criteria: ''
  }),
  
  // 课程管理
  getCourse: (courseId) => api.get(`/teacher/courses/${courseId}`),
  enrollStudent: (courseId, studentData) => api.post(`/teacher/courses/${courseId}/enroll`, studentData),
  unenrollStudent: (courseId, studentId) => api.delete(`/teacher/courses/${courseId}/enroll/${studentId}`),
  
  // 查看提交
  getSubmissions: (assignmentId) => api.get(`/teacher/assignments/${assignmentId}/submissions`),
  
  // 保存生成的作业
  saveGeneratedAssignment: (assignmentData) => api.post('/save_generated_assignment', assignmentData)
}

export const studentAPI = {
  // 获取学生课程列表（如果后端有这个接口）
  getCourses: () => api.get('/student/courses'),
  
  // 获取课程详情（如果后端有这个接口）
  getCourse: (courseId) => api.get(`/student/courses/${courseId}`),
  
  // 获取作业列表（如果后端有这个接口）
  getAssignments: (courseId) => api.get(`/student/courses/${courseId}/assignments`),
  
  // 获取作业详情（如果后端有这个接口）
  getAssignment: (assignmentId) => api.get(`/student/assignments/${assignmentId}`),
  
  // 提交作业（如果后端有这个接口）
  submitAssignment: (assignmentId, submissionData) => api.post(`/student/assignments/${assignmentId}/submit`, submissionData),
  
  // 获取我的提交记录（如果后端有这个接口）
  getMySubmissions: () => api.get('/student/submissions'),
  
  // 获取提交详情（如果后端有这个接口）
  getSubmission: (submissionId) => api.get(`/student/submissions/${submissionId}`)
} 