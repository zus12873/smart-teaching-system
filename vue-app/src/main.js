import { createApp } from 'vue'
import router from './router'
import App from './App.vue'

// 引入 Bootstrap CSS 和 JS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'

// 引入自定义样式
import './style.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
