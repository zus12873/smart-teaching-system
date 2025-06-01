// 前端功能测试脚本
// 在浏览器控制台中运行此脚本来测试各种功能

console.log('�� 开始前端功能测试...')

// 检测API基础URL
const API_BASE = window.location.origin.includes('localhost:5173') ? '/api' : 'http://127.0.0.1:5000/api'
console.log('🌐 API基础URL:', API_BASE)

// 测试API连接
async function testAPIConnection() {
  console.log('\n📡 测试API连接...')
  
  try {
    const response = await fetch(`${API_BASE}/health`)
    const data = await response.json()
    console.log('✅ API健康检查成功:', data)
    return true
  } catch (error) {
    console.error('❌ API连接失败:', error)
    return false
  }
}

// 测试登录功能
async function testLogin(username = 'admin', password = 'admin') {
  console.log(`\n🔐 测试登录功能 (${username})...`)
  
  try {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ username, password })
    })
    
    const data = await response.json()
    console.log('✅ 登录测试结果:', data)
    return data.success
  } catch (error) {
    console.error('❌ 登录测试失败:', error)
    return false
  }
}

// 测试获取当前用户
async function testCurrentUser() {
  console.log('\n👤 测试获取当前用户...')
  
  try {
    const response = await fetch(`${API_BASE}/auth/current`, {
      credentials: 'include'
    })
    
    const data = await response.json()
    console.log('✅ 当前用户信息:', data)
    return data.success
  } catch (error) {
    console.error('❌ 获取用户信息失败:', error)
    return false
  }
}

// 测试管理员仪表板
async function testAdminDashboard() {
  console.log('\n🔧 测试管理员仪表板...')
  
  try {
    const response = await fetch(`${API_BASE}/admin/dashboard`, {
      credentials: 'include'
    })
    
    const data = await response.json()
    console.log('✅ 管理员仪表板数据:', data)
    return data.success
  } catch (error) {
    console.error('❌ 管理员仪表板测试失败:', error)
    return false
  }
}

// 测试教师课程API
async function testTeacherCourses() {
  console.log('\n📚 测试教师课程API...')
  
  try {
    const response = await fetch(`${API_BASE}/teacher_courses_api`, {
      credentials: 'include'
    })
    
    const data = await response.json()
    console.log('✅ 教师课程数据:', data)
    return data.success
  } catch (error) {
    console.error('❌ 教师课程API测试失败:', error)
    return false
  }
}

// 运行完整测试套件
async function runFullTest() {
  console.log('🚀 开始完整功能测试...')
  
  const results = {
    apiConnection: await testAPIConnection(),
    adminLogin: await testLogin('admin', 'admin'),
    currentUser: await testCurrentUser(),
    adminDashboard: await testAdminDashboard(),
  }
  
  // 测试教师登录
  console.log('\n--- 切换到教师账号 ---')
  results.teacherLogin = await testLogin('teacher', 'teacher')
  results.teacherCourses = await testTeacherCourses()
  
  // 测试学生登录
  console.log('\n--- 切换到学生账号 ---')
  results.studentLogin = await testLogin('student', 'student')
  
  console.log('\n📊 测试结果汇总:')
  console.table(results)
  
  const successCount = Object.values(results).filter(Boolean).length
  const totalCount = Object.keys(results).length
  
  console.log(`\n🎯 测试完成: ${successCount}/${totalCount} 通过`)
  
  if (successCount === totalCount) {
    console.log('🎉 所有测试都通过了！')
  } else {
    console.log('⚠️ 部分测试失败，请检查问题')
  }
  
  return results
}

// 测试本地存储功能
function testLocalStorage() {
  console.log('\n💾 测试本地存储功能...')
  
  try {
    // 测试设置和获取
    const testData = { test: true, timestamp: Date.now() }
    localStorage.setItem('test_data', JSON.stringify(testData))
    
    const retrieved = JSON.parse(localStorage.getItem('test_data'))
    console.log('✅ 本地存储测试通过:', retrieved)
    
    // 清理
    localStorage.removeItem('test_data')
    return true
  } catch (error) {
    console.error('❌ 本地存储测试失败:', error)
    return false
  }
}

// 测试Vue路由（如果在Vue应用中运行）
function testVueRouter() {
  console.log('\n🗺️ 测试Vue路由...')
  
  if (typeof window !== 'undefined' && window.Vue) {
    try {
      console.log('当前路由:', window.location.pathname)
      console.log('✅ Vue路由可用')
      return true
    } catch (error) {
      console.error('❌ Vue路由测试失败:', error)
      return false
    }
  } else {
    console.log('ℹ️ 不在Vue环境中，跳过路由测试')
    return null
  }
}

// 导出测试函数
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    testAPIConnection,
    testLogin,
    testCurrentUser,
    testAdminDashboard,
    testTeacherCourses,
    testLocalStorage,
    testVueRouter,
    runFullTest
  }
}

// 如果在浏览器中运行，自动开始测试
if (typeof window !== 'undefined') {
  console.log('🌐 在浏览器环境中检测到，可以运行以下命令:')
  console.log('- runFullTest() - 运行完整测试')
  console.log('- testAPIConnection() - 测试API连接')
  console.log('- testLogin("admin", "admin") - 测试登录')
  console.log('- testLocalStorage() - 测试本地存储')
} 